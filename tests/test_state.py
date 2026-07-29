import json

import pytest

from kimlik.state import STATE_FILE, create_state, load_state, save_state

MODELS = {
    "openai_phase1": "gpt-x-pro",
    "openai_phase2": "gpt-x",
    "anthropic": "claude-x",
    "parallel_processor": "ultra8x",
}


@pytest.fixture
def state(tmp_path):
    return create_state("right lung", "metastatic osteosarcoma", str(tmp_path), MODELS)


def test_create_state_records_inputs_and_models(state):
    assert state["biopsy_site"] == "right lung"
    assert state["tumor_diagnosis"] == "metastatic osteosarcoma"
    assert state["models"] == MODELS


def test_create_state_has_every_phase_and_provider(state):
    assert set(state["phase1"]) == {"openai", "parallel", "anthropic"}
    assert set(state["phase2"]) == {"openai", "anthropic"}
    assert set(state["phase3"]) == {"anthropic"}


def test_all_tasks_start_pending(state):
    for phase in ("phase1", "phase2", "phase3"):
        for task in state[phase].values():
            assert task["status"] == "pending"
            assert task["output_file"] is None
            assert task["task_id"] is None


def test_tasks_are_not_shared_objects(state):
    """A shallow-copied task dict would make one provider's status clobber another's."""
    state["phase1"]["openai"]["status"] = "running"
    assert state["phase1"]["parallel"]["status"] == "pending"
    assert state["phase2"]["openai"]["status"] == "pending"


def test_save_then_load_round_trips(tmp_path, state):
    save_state(tmp_path, state)
    assert load_state(tmp_path) == state


def test_load_returns_none_when_absent(tmp_path):
    assert load_state(tmp_path) is None


def test_save_leaves_no_temp_file_behind(tmp_path, state):
    save_state(tmp_path, state)
    assert [p.name for p in tmp_path.iterdir()] == [STATE_FILE]


def test_save_overwrites_previous_state(tmp_path, state):
    save_state(tmp_path, state)
    state["phase1"]["openai"]["status"] = "completed"
    save_state(tmp_path, state)
    assert load_state(tmp_path)["phase1"]["openai"]["status"] == "completed"


def test_load_migrates_state_written_before_phase3(tmp_path, state):
    del state["phase3"]
    (tmp_path / STATE_FILE).write_text(json.dumps(state), encoding="utf-8")

    loaded = load_state(tmp_path)
    assert loaded["phase3"]["anthropic"]["status"] == "pending"
    # Migration is persisted, not just returned.
    assert "phase3" in json.loads((tmp_path / STATE_FILE).read_text())


def test_load_migrates_state_written_before_models_were_recorded(tmp_path, state):
    del state["models"]
    (tmp_path / STATE_FILE).write_text(json.dumps(state), encoding="utf-8")
    assert load_state(tmp_path)["models"] == {}


def test_migration_preserves_completed_work(tmp_path, state):
    """Resuming an old run must not discard results already paid for."""
    state["phase1"]["parallel"].update(status="completed", output_file="phase1_parallel.md")
    del state["phase3"]
    (tmp_path / STATE_FILE).write_text(json.dumps(state), encoding="utf-8")

    loaded = load_state(tmp_path)
    assert loaded["phase1"]["parallel"]["status"] == "completed"
    assert loaded["phase1"]["parallel"]["output_file"] == "phase1_parallel.md"
