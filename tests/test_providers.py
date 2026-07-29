"""Provider tests. Every SDK call is faked — these never touch the network."""

import pytest

from kimlik.providers import anthropic_provider, openai_provider, parallel_provider

# ---------------------------------------------------------------------------
# Anthropic
# ---------------------------------------------------------------------------


class _Block:
    def __init__(self, text):
        self.type = "text"
        self.text = text


class _Response:
    def __init__(self, text, stop_reason):
        self.content = [_Block(text)]
        self.stop_reason = stop_reason


class _Stream:
    def __init__(self, response):
        self._response = response

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def get_final_message(self):
        return self._response


class _Messages:
    def __init__(self, response, recorder):
        self._response = response
        self._recorder = recorder

    def stream(self, **kwargs):
        self._recorder.append(kwargs)
        return _Stream(self._response)


@pytest.fixture
def anthropic_calls(monkeypatch):
    """Patch the Anthropic client; returns the list of request kwargs seen."""
    calls = []

    def install(text="report body", stop_reason="end_turn"):
        response = _Response(text, stop_reason)

        class _FakeClient:
            def __init__(self, **_):
                self.messages = _Messages(response, calls)

        monkeypatch.setattr(anthropic_provider.anthropic, "AsyncAnthropic", _FakeClient)
        return calls

    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    return install


async def test_anthropic_returns_text_on_end_turn(anthropic_calls):
    anthropic_calls(text="the report")
    assert await anthropic_provider.run_anthropic("p", "claude-x") == "the report"


async def test_anthropic_uses_the_model_it_is_given(anthropic_calls):
    calls = anthropic_calls()
    await anthropic_provider.run_anthropic("p", "claude-custom")
    assert calls[0]["model"] == "claude-custom"


async def test_anthropic_phase1_enables_tools(anthropic_calls):
    calls = anthropic_calls()
    await anthropic_provider.run_anthropic("p", "claude-x", use_tools=True)
    tool_names = {t.get("name") for t in calls[0]["tools"]}
    assert {"web_search", "pubmed_search"} <= tool_names


async def test_anthropic_phase2_sends_no_tools(anthropic_calls):
    calls = anthropic_calls()
    await anthropic_provider.run_anthropic("p", "claude-x", use_tools=False)
    assert "tools" not in calls[0]


async def test_anthropic_truncation_is_reported_not_swallowed(anthropic_calls, capsys):
    """Regression: max_tokens used to break silently, returning a partial report
    whose reference list had been cut off."""
    anthropic_calls(text="cut off mid-sen", stop_reason="max_tokens")

    result = await anthropic_provider.run_anthropic("p", "claude-x", use_tools=False)

    assert result == "cut off mid-sen"  # partial output still returned
    warning = capsys.readouterr().out.lower()
    assert "warning" in warning
    assert "truncat" in warning


async def test_anthropic_token_ceiling_is_generous_enough_for_a_full_report(anthropic_calls):
    """These reports run tens of thousands of tokens; a low ceiling silently
    drops the trailing bibliography."""
    calls = anthropic_calls()
    await anthropic_provider.run_anthropic("p", "claude-x")
    assert calls[0]["max_tokens"] >= 64_000


# ---------------------------------------------------------------------------
# OpenAI
# ---------------------------------------------------------------------------


class _OpenAIResponse:
    def __init__(self, status="completed", text="body", reason="max_output_tokens"):
        self.id = "resp_123"
        self.status = status
        self.output_text = text
        self.incomplete_details = type("D", (), {"reason": reason})()


@pytest.fixture
def openai_client(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    calls = []

    def install(response=None):
        resp = response or _OpenAIResponse()

        class _Responses:
            async def create(self, **kwargs):
                calls.append(kwargs)
                return resp

            async def retrieve(self, _id):
                return resp

        class _FakeClient:
            def __init__(self, **_):
                self.responses = _Responses()

        monkeypatch.setattr(openai_provider, "AsyncOpenAI", _FakeClient)
        return calls

    return install


async def test_openai_passes_max_tokens_through(openai_client):
    """Regression: the budget used to be chosen by comparing the model name to a
    constant, so overriding the model silently shrank the Phase 1 ceiling."""
    calls = openai_client()
    await openai_provider.submit_openai_task("p", "any-model-name", 12_345)
    assert calls[0]["max_output_tokens"] == 12_345


async def test_openai_budget_follows_the_phase_not_the_model(openai_client):
    calls = openai_client()
    await openai_provider.submit_openai_task("p", "same-model", openai_provider.PHASE1_MAX_TOKENS)
    await openai_provider.submit_openai_task("p", "same-model", openai_provider.PHASE2_MAX_TOKENS)
    assert calls[0]["max_output_tokens"] != calls[1]["max_output_tokens"]


async def test_openai_phase1_budget_exceeds_phase2(openai_client):
    assert openai_provider.PHASE1_MAX_TOKENS > openai_provider.PHASE2_MAX_TOKENS


async def test_openai_submits_in_background_mode(openai_client):
    calls = openai_client()
    await openai_provider.submit_openai_task("p", "m", 100)
    assert calls[0]["background"] is True


async def test_openai_incomplete_response_warns_and_returns_partial(openai_client, capsys):
    openai_client(_OpenAIResponse(status="incomplete", text="partial body"))
    result = await openai_provider.get_openai_result("resp_123")
    assert result == "partial body"
    assert "warning" in capsys.readouterr().out.lower()


async def test_openai_incomplete_warning_has_no_unrendered_markup(openai_client, capsys):
    """This goes through plain print(), so rich tags would show up literally."""
    openai_client(_OpenAIResponse(status="incomplete"))
    await openai_provider.get_openai_result("resp_123")
    assert "[yellow]" not in capsys.readouterr().out


@pytest.mark.parametrize("status", ["failed", "cancelled"])
async def test_openai_terminal_failure_raises(openai_client, status):
    openai_client(_OpenAIResponse(status=status))
    with pytest.raises(RuntimeError, match=status):
        await openai_provider.get_openai_result("resp_123")


# ---------------------------------------------------------------------------
# Parallel.ai
# ---------------------------------------------------------------------------


@pytest.fixture
def parallel_client(monkeypatch):
    monkeypatch.setenv("PARALLEL_API_KEY", "test-key")
    monkeypatch.setattr(parallel_provider.time, "sleep", lambda _: None)
    state = {"create_kwargs": [], "results": []}

    def install(results):
        state["results"] = list(results)

        class _TaskRun:
            def create(self, **kwargs):
                state["create_kwargs"].append(kwargs)
                return type("R", (), {"run_id": "trun_123"})()

            def result(self, run_id, api_timeout=None):
                item = state["results"].pop(0)
                if isinstance(item, Exception):
                    raise item
                return type("R", (), {"output": type("O", (), {"content": item})()})()

        class _FakeParallel:
            def __init__(self, **_):
                self.task_run = _TaskRun()

        monkeypatch.setattr(parallel_provider, "Parallel", _FakeParallel)
        return state

    return install


def test_parallel_uses_the_processor_it_is_given(parallel_client):
    state = parallel_client([])
    parallel_provider.submit_parallel_task("prompt", "ultra2x")
    assert state["create_kwargs"][0]["processor"] == "ultra2x"


def test_parallel_returns_run_id_immediately(parallel_client):
    parallel_client([])
    assert parallel_provider.submit_parallel_task("prompt", "ultra8x") == "trun_123"


def test_parallel_returns_content_when_ready(parallel_client):
    parallel_client(["the markdown"])
    assert parallel_provider.get_parallel_result("trun_123") == "the markdown"


@pytest.mark.parametrize(
    "message",
    ["Request timed out", "408 Run still active", "Run Still Active"],
)
def test_parallel_retries_transient_errors(parallel_client, message):
    """A long ultra8x task reports 'still running' as an exception; retrying is
    the difference between a result and a lost multi-hour run."""
    parallel_client([Exception(message), "the markdown"])
    assert parallel_provider.get_parallel_result("trun_123") == "the markdown"


def test_parallel_propagates_real_errors(parallel_client):
    parallel_client([Exception("401 invalid api key")])
    with pytest.raises(Exception, match="invalid api key"):
        parallel_provider.get_parallel_result("trun_123")


def test_parallel_coerces_non_string_content(parallel_client):
    parallel_client([{"unexpected": "shape"}])
    assert isinstance(parallel_provider.get_parallel_result("trun_123"), str)
