import asyncio
import os
import time

import httpx
from openai import AsyncOpenAI

# Phase 1 uses heavy reasoning (often 25K+ reasoning tokens); give it room.
# Passed explicitly by the caller — the budget follows the phase, not the model
# name, so overriding a model never silently changes the token ceiling.
PHASE1_MAX_TOKENS = 100_000
PHASE2_MAX_TOKENS = 64_000
# Short HTTP timeout — just for submit and retrieve calls, not for waiting.
_HTTP_TIMEOUT = httpx.Timeout(timeout=60.0, connect=10.0)
_POLL_INTERVAL = 30   # seconds between status checks
_POLL_TIMEOUT = 7_200  # 2 hours total budget
# Reasoning models can think for many minutes with no output; say something
# periodically so the run does not look frozen.
_HEARTBEAT_SECONDS = 300


def _make_client() -> AsyncOpenAI:
    return AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"], timeout=_HTTP_TIMEOUT)


async def submit_openai_task(prompt: str, model: str, max_tokens: int) -> str:
    """Submit in background mode and return the response_id immediately."""
    client = _make_client()
    response = await client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=max_tokens,
        background=True,
    )
    return response.id


async def get_openai_result(response_id: str) -> str:
    """Poll until the background response completes and return the text."""
    client = _make_client()
    started = time.time()
    deadline = started + _POLL_TIMEOUT
    next_heartbeat = started + _HEARTBEAT_SECONDS

    while True:
        if time.time() > deadline:
            raise TimeoutError(
                f"OpenAI response {response_id} did not complete within "
                f"{_POLL_TIMEOUT // 60} minutes"
            )
        response = await client.responses.retrieve(response_id)

        if response.status == "completed":
            return response.output_text or ""

        if response.status == "incomplete":
            # Hit max_output_tokens — accept what we have rather than fail.
            reason = getattr(response.incomplete_details, "reason", "unknown")
            print(f"Warning: OpenAI response {response_id} incomplete ({reason})")
            return response.output_text or ""

        if response.status in ("failed", "cancelled"):
            raise RuntimeError(
                f"OpenAI response {response_id} ended with status: {response.status}"
            )

        now = time.time()
        if now >= next_heartbeat:
            print(f"  OpenAI still working: {int(now - started) // 60} min elapsed.")
            next_heartbeat = now + _HEARTBEAT_SECONDS

        await asyncio.sleep(_POLL_INTERVAL)


async def run_openai(prompt: str, model: str, max_tokens: int) -> str:
    """One-shot helper used for Phase 2 (shorter responses, no state needed)."""
    response_id = await submit_openai_task(prompt, model, max_tokens)
    return await get_openai_result(response_id)
