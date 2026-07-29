"""Timing reported in the run summary."""

import pytest

from kimlik.cli import format_duration, task_duration, wall_clock


def task(started=None, completed=None):
    return {"started_at": started, "completed_at": completed}


@pytest.mark.parametrize(
    ("seconds", "expected"),
    [
        (0, "0s"),
        (45, "45s"),
        (60, "1m 00s"),
        (95, "1m 35s"),
        (2_640, "44m 00s"),   # the Parallel.ai deep-research run
        (3_600, "1h 00m"),
        (5_130, "1h 25m"),
    ],
)
def test_durations_read_naturally(seconds, expected):
    assert format_duration(seconds) == expected


def test_task_duration_from_timestamps():
    assert task_duration(
        task("2026-07-29T00:22:00+00:00", "2026-07-29T00:31:19+00:00")
    ) == "9m 19s"


@pytest.mark.parametrize(
    "t",
    [
        task(),                                          # never started
        task("2026-07-29T00:22:00+00:00", None),         # still running
        task(None, "2026-07-29T00:31:19+00:00"),         # no start recorded
        task("not-a-timestamp", "also-not"),             # corrupt state file
    ],
)
def test_incomplete_or_corrupt_timing_is_not_fatal(t):
    """The summary prints after failures too; it must never raise."""
    assert task_duration(t) == "-"


def test_wall_clock_spans_first_start_to_last_finish():
    """Phase 1 runs concurrently, so wall time is the span, not the sum."""
    state = {
        "phase1": {
            "openai": task("2026-07-29T00:00:00+00:00", "2026-07-29T00:12:00+00:00"),
            "parallel": task("2026-07-29T00:00:00+00:00", "2026-07-29T00:44:00+00:00"),
            "anthropic": task("2026-07-29T00:00:00+00:00", "2026-07-29T00:09:00+00:00"),
        },
        "phase2": {
            "openai": task("2026-07-29T00:44:00+00:00", "2026-07-29T00:47:00+00:00"),
            "anthropic": task("2026-07-29T00:44:00+00:00", "2026-07-29T00:52:00+00:00"),
        },
        "phase3": {
            "anthropic": task("2026-07-29T00:52:00+00:00", "2026-07-29T00:59:00+00:00"),
        },
    }
    # Sum of every task is over 2 hours; the actual run took 59 minutes.
    assert wall_clock(state) == "59m 00s"


def test_wall_clock_handles_a_run_that_never_started():
    assert wall_clock({"phase1": {"openai": task()}}) == "-"


def test_wall_clock_ignores_phases_absent_from_an_older_state_file():
    state = {"phase1": {"openai": task("2026-07-29T00:00:00+00:00", "2026-07-29T00:05:00+00:00")}}
    assert wall_clock(state) == "5m 00s"


def test_parallel_heartbeat_is_not_blocked_by_its_own_long_poll():
    """result() long-polls, and nothing prints while it blocks.

    If the per-call ceiling exceeds the heartbeat interval, the heartbeat
    silently degrades to the ceiling and the terminal goes quiet for that long.
    """
    from kimlik.providers import parallel_provider as pp

    assert pp._PER_CALL_TIMEOUT <= pp._HEARTBEAT_SECONDS
