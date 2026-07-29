import os
import time
from parallel import Parallel

_POLL_TIMEOUT_SECONDS = 7_200  # 2-hour budget, sized for the ultra8x processor
_PER_CALL_TIMEOUT = 1_500      # ceiling per result() call; SDK enforces ~1800 s internally
_RETRY_SLEEP = 30              # seconds to wait between retries


def submit_parallel_task(prompt: str, processor: str) -> str:
    """Submit a deep-research task and return the run_id immediately."""
    client = Parallel(api_key=os.environ["PARALLEL_API_KEY"])
    task_run = client.task_run.create(
        input=prompt,
        processor=processor,
        task_spec={"output_schema": {"type": "text"}},
    )
    return task_run.run_id


# Substrings in exception messages that mean "not done yet, keep polling".
_TRANSIENT_ERRORS = ("timed out", "run still active", "408")


def get_parallel_result(run_id: str) -> str:
    """Poll until the task completes and return the markdown content.

    Parallel.ai's result() either returns when done or raises when the
    per-call timeout fires ("timed out") or the task is still running ("408 /
    Run still active"). Both are transient — we sleep briefly and retry until
    the 2-hour budget runs out.
    """
    client = Parallel(api_key=os.environ["PARALLEL_API_KEY"])
    deadline = time.time() + _POLL_TIMEOUT_SECONDS

    while time.time() < deadline:
        try:
            result = client.task_run.result(run_id, api_timeout=_PER_CALL_TIMEOUT)
            content = result.output.content
            return content if isinstance(content, str) else str(content)
        except Exception as exc:
            msg = str(exc).lower()
            if any(s in msg for s in _TRANSIENT_ERRORS):
                time.sleep(_RETRY_SLEEP)
                continue
            raise

    raise TimeoutError(
        f"Parallel.ai task {run_id} did not complete within {_POLL_TIMEOUT_SECONDS // 60} minutes"
    )
