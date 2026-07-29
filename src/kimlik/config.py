"""Model selection for every provider.

Vendors ship new models faster than this tool changes, so nothing here is
hard-coded at the call site. Each model is resolved once at startup with the
precedence: CLI flag > environment variable > built-in default.

The resolved config is recorded in the run's state file, so a finished run
always says which models produced it.
"""

import os
from dataclasses import asdict, dataclass

# Built-in defaults — the newest models verified to work with this pipeline.
DEFAULT_OPENAI_PHASE1_MODEL = "gpt-5.5-pro"
DEFAULT_OPENAI_PHASE2_MODEL = "gpt-5.5"
DEFAULT_ANTHROPIC_MODEL = "claude-opus-5"
DEFAULT_PARALLEL_PROCESSOR = "ultra8x"

_DEFAULTS: dict[str, str] = {
    "openai_phase1": DEFAULT_OPENAI_PHASE1_MODEL,
    "openai_phase2": DEFAULT_OPENAI_PHASE2_MODEL,
    "anthropic": DEFAULT_ANTHROPIC_MODEL,
    "parallel_processor": DEFAULT_PARALLEL_PROCESSOR,
}

_ENV_VARS: dict[str, str] = {
    "openai_phase1": "KIMLIK_OPENAI_PHASE1_MODEL",
    "openai_phase2": "KIMLIK_OPENAI_PHASE2_MODEL",
    "anthropic": "KIMLIK_ANTHROPIC_MODEL",
    "parallel_processor": "KIMLIK_PARALLEL_PROCESSOR",
}


@dataclass(frozen=True)
class ModelConfig:
    """The models used for a single run."""

    openai_phase1: str
    openai_phase2: str
    anthropic: str
    parallel_processor: str

    @classmethod
    def resolve(cls, **overrides: str | None) -> "ModelConfig":
        """Build a config from CLI overrides, falling back to env vars, then defaults.

        Any override that is None or empty is treated as "not supplied".
        """
        unknown = set(overrides) - set(_DEFAULTS)
        if unknown:
            raise ValueError(f"Unknown model settings: {sorted(unknown)}")

        return cls(
            **{
                field: (overrides.get(field) or os.getenv(_ENV_VARS[field]) or default)
                for field, default in _DEFAULTS.items()
            }
        )

    def phase1_labels(self) -> dict[str, str]:
        """Labels attributing each Phase 1 report to the model that wrote it."""
        return {
            "openai": f"OpenAI {self.openai_phase1}",
            "parallel": f"Parallel.ai {self.parallel_processor}",
            "anthropic": f"Anthropic {self.anthropic}",
        }

    def phase2_labels(self) -> dict[str, str]:
        """Labels for the two consensus reports Phase 3 merges.

        Distinct from phase1_labels because Phase 2 uses the cheaper OpenAI
        model — attributing a consensus report to the Phase 1 model would be wrong.
        """
        return {
            "openai": f"OpenAI {self.openai_phase2}",
            "anthropic": f"Anthropic {self.anthropic}",
        }

    def as_dict(self) -> dict[str, str]:
        return asdict(self)
