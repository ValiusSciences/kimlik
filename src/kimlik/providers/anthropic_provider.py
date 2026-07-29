import asyncio
import os
import httpx
import anthropic

# These reports are long: dense marker tables plus a full bibliography. At the
# old 16K ceiling every Anthropic response was silently cut off mid-table, which
# also dropped the reference list the prompt explicitly asks for.
_MAX_TOKENS = 64_000
_MAX_TOOL_TURNS = 30

# Anthropic-hosted web search — executed server-side, no client fetch needed.
_WEB_SEARCH_TOOL: dict = {
    "type": "web_search_20250305",
    "name": "web_search",
}

# PubMed via NCBI E-utilities — executed client-side in the tool loop.
_PUBMED_TOOL: dict = {
    "name": "pubmed_search",
    "description": (
        "Search PubMed for peer-reviewed scientific articles on genes, cell types, "
        "biomarkers, and cancer biology. Use this to find specific publications and "
        "their PMIDs, authors, and abstracts."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "PubMed search query (supports MeSH terms and Boolean operators)",
            },
            "max_results": {
                "type": "integer",
                "default": 15,
                "description": "Maximum number of abstracts to return (max 50)",
            },
        },
        "required": ["query"],
    },
}


async def _pubmed_search(query: str, max_results: int = 15) -> str:
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    max_results = min(max_results, 50)

    async with httpx.AsyncClient(timeout=30) as client:
        # NCBI allows 3 req/s without an API key; retry 429s with backoff.
        for attempt in range(4):
            search_resp = await client.get(
                f"{base}/esearch.fcgi",
                params={"db": "pubmed", "term": query, "retmax": max_results, "retmode": "json"},
            )
            if search_resp.status_code == 429:
                await asyncio.sleep(2 ** attempt)
                continue
            search_resp.raise_for_status()
            break
        else:
            return f"PubMed rate limit exceeded for query: {query!r}"

        ids = search_resp.json()["esearchresult"]["idlist"]
        if not ids:
            return f"No PubMed results found for query: {query!r}"

        await asyncio.sleep(0.4)  # stay under 3 req/s

        for attempt in range(4):
            fetch_resp = await client.get(
                f"{base}/efetch.fcgi",
                params={"db": "pubmed", "id": ",".join(ids), "rettype": "abstract", "retmode": "text"},
            )
            if fetch_resp.status_code == 429:
                await asyncio.sleep(2 ** attempt)
                continue
            fetch_resp.raise_for_status()
            break
        else:
            return f"PubMed rate limit exceeded fetching abstracts for query: {query!r}"

        return fetch_resp.text[:12_000]


def _extract_text(content_blocks: list) -> str:
    return "\n\n".join(
        block.text for block in content_blocks if hasattr(block, "text") and block.text
    )


async def run_anthropic(prompt: str, model: str, use_tools: bool = True) -> str:
    """Run a prompt against the given Anthropic model.

    Phase 1 (use_tools=True): enables web_search and pubmed_search so the model
    can look up current literature before writing its report.
    Phase 2 (use_tools=False): pure synthesis — no external lookups needed.
    """
    client = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    messages: list[dict] = [{"role": "user", "content": prompt}]
    tools = [_WEB_SEARCH_TOOL, _PUBMED_TOOL] if use_tools else []

    for _ in range(_MAX_TOOL_TURNS):
        kwargs: dict = {
            "model": model,
            "max_tokens": _MAX_TOKENS,
            "messages": messages,
        }
        if tools:
            kwargs["tools"] = tools

        # Streaming is mandatory at this token ceiling: the SDK rejects
        # non-streaming requests that could run past 10 minutes. We only need
        # the assembled message, not the incremental deltas.
        async with client.messages.stream(**kwargs) as stream:
            response = await stream.get_final_message()

        if response.stop_reason == "end_turn":
            return _extract_text(response.content)

        if response.stop_reason == "max_tokens":
            # Truncated mid-document. Return what we have so a long run is not
            # lost, but say so loudly — a silent partial report looks complete
            # while missing whole sections (typically the trailing references).
            print(
                f"WARNING: Anthropic response hit the {_MAX_TOKENS} token ceiling "
                "and was truncated. The report is incomplete — raise _MAX_TOKENS "
                "in anthropic_provider.py and re-run this phase."
            )
            break

        if response.stop_reason != "tool_use":
            # Unexpected stop — return whatever text we have
            break

        # Handle tool calls
        messages.append({"role": "assistant", "content": response.content})
        tool_results = []

        for block in response.content:
            if not hasattr(block, "type") or block.type != "tool_use":
                continue

            if block.name == "pubmed_search":
                result_content = await _pubmed_search(
                    query=block.input.get("query", ""),
                    max_results=block.input.get("max_results", 15),
                )
            elif block.name == "web_search":
                # web_search_20250305 is server-side: Anthropic's infrastructure
                # handles the fetch transparently. We still need to return a
                # tool_result block; the platform populates the actual content.
                result_content = ""
            else:
                result_content = f"Tool '{block.name}' is not implemented."

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result_content,
            })

        if tool_results:
            messages.append({"role": "user", "content": tool_results})

    return _extract_text(response.content)
