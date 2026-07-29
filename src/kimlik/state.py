import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

STATE_FILE = "kimlik_state.json"


def _make_task() -> dict:
    return {
        "status": "pending",
        "output_file": None,
        "task_id": None,
        "started_at": None,
        "completed_at": None,
        "error": None,
    }


def create_state(
    biopsy_site: str,
    tumor_diagnosis: str,
    output_dir: str,
    models: dict[str, str],
) -> dict:
    return {
        "biopsy_site": biopsy_site,
        "tumor_diagnosis": tumor_diagnosis,
        "output_dir": output_dir,
        "models": models,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "phase1": {
            "openai": _make_task(),
            "parallel": _make_task(),
            "anthropic": _make_task(),
        },
        "phase2": {
            "openai": _make_task(),
            "anthropic": _make_task(),
        },
        "phase3": {
            "anthropic": _make_task(),
        },
    }


def load_state(output_dir: Path) -> Optional[dict]:
    path = output_dir / STATE_FILE
    if not path.exists():
        return None
    state = json.loads(path.read_text(encoding="utf-8"))
    # Migrate state files created before Phase 3 was added.
    if "phase3" not in state:
        state["phase3"] = {"anthropic": _make_task()}
        save_state(output_dir, state)
    # Migrate state files created before models were recorded.
    state.setdefault("models", {})
    return state


def save_state(output_dir: Path, state: dict) -> None:
    path = output_dir / STATE_FILE
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.rename(path)
