import dataclasses

import pytest

from kimlik.config import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_OPENAI_PHASE1_MODEL,
    DEFAULT_OPENAI_PHASE2_MODEL,
    DEFAULT_PARALLEL_PROCESSOR,
    ModelConfig,
)

ENV_VARS = [
    "KIMLIK_OPENAI_PHASE1_MODEL",
    "KIMLIK_OPENAI_PHASE2_MODEL",
    "KIMLIK_ANTHROPIC_MODEL",
    "KIMLIK_PARALLEL_PROCESSOR",
]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    """Model env vars must not leak in from the developer's shell."""
    for var in ENV_VARS:
        monkeypatch.delenv(var, raising=False)


def test_defaults_when_nothing_supplied():
    cfg = ModelConfig.resolve()
    assert cfg.openai_phase1 == DEFAULT_OPENAI_PHASE1_MODEL
    assert cfg.openai_phase2 == DEFAULT_OPENAI_PHASE2_MODEL
    assert cfg.anthropic == DEFAULT_ANTHROPIC_MODEL
    assert cfg.parallel_processor == DEFAULT_PARALLEL_PROCESSOR


def test_env_var_overrides_default(monkeypatch):
    monkeypatch.setenv("KIMLIK_ANTHROPIC_MODEL", "claude-from-env")
    assert ModelConfig.resolve().anthropic == "claude-from-env"


def test_cli_override_beats_env_var(monkeypatch):
    monkeypatch.setenv("KIMLIK_ANTHROPIC_MODEL", "claude-from-env")
    assert ModelConfig.resolve(anthropic="claude-from-cli").anthropic == "claude-from-cli"


@pytest.mark.parametrize("empty", [None, ""])
def test_unsupplied_cli_value_falls_through_to_env(monkeypatch, empty):
    """Typer passes None for an unused flag; that must not shadow the env var."""
    monkeypatch.setenv("KIMLIK_ANTHROPIC_MODEL", "claude-from-env")
    assert ModelConfig.resolve(anthropic=empty).anthropic == "claude-from-env"


def test_each_setting_is_independently_overridable(monkeypatch):
    monkeypatch.setenv("KIMLIK_OPENAI_PHASE1_MODEL", "p1")
    monkeypatch.setenv("KIMLIK_PARALLEL_PROCESSOR", "ultra2x")
    cfg = ModelConfig.resolve(openai_phase2="p2")
    assert (cfg.openai_phase1, cfg.openai_phase2) == ("p1", "p2")
    assert cfg.parallel_processor == "ultra2x"
    assert cfg.anthropic == DEFAULT_ANTHROPIC_MODEL  # untouched


def test_unknown_setting_is_rejected():
    """Guards against a silently-ignored typo like anthropic_model=..."""
    with pytest.raises(ValueError, match="anthropic_model"):
        ModelConfig.resolve(anthropic_model="claude-opus-5")


def test_phase1_and_phase2_labels_use_different_openai_models():
    """A Phase 2 consensus report must not be attributed to the Phase 1 model."""
    cfg = ModelConfig.resolve(openai_phase1="big-model", openai_phase2="small-model")
    assert cfg.phase1_labels()["openai"] == "OpenAI big-model"
    assert cfg.phase2_labels()["openai"] == "OpenAI small-model"


def test_phase1_labels_cover_every_phase1_provider():
    assert set(ModelConfig.resolve().phase1_labels()) == {"openai", "parallel", "anthropic"}


def test_phase2_labels_exclude_parallel():
    """Parallel.ai only runs in Phase 1, so it must not appear in Phase 2 attribution."""
    assert set(ModelConfig.resolve().phase2_labels()) == {"openai", "anthropic"}


def test_as_dict_is_json_serialisable_and_round_trips():
    import json

    cfg = ModelConfig.resolve(anthropic="x")
    assert ModelConfig(**json.loads(json.dumps(cfg.as_dict()))) == cfg


def test_config_is_immutable():
    cfg = ModelConfig.resolve()
    with pytest.raises(dataclasses.FrozenInstanceError):
        cfg.anthropic = "mutated"
