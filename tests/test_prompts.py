from kimlik.config import ModelConfig
from kimlik.prompts import format_consolidation, format_final, format_phase1

SITE = "right lung"
DX = "metastatic osteosarcoma (primary: distal femur)"


def test_phase1_prompt_carries_both_inputs():
    prompt = format_phase1(SITE, DX)
    assert SITE in prompt
    assert DX in prompt
    assert "{" not in prompt  # every placeholder substituted


def test_phase1_prompt_asks_for_references():
    assert "reference" in format_phase1(SITE, DX).lower()


def test_consolidation_includes_every_report_and_its_label():
    reports = {"openai": "REPORT_A", "parallel": "REPORT_B", "anthropic": "REPORT_C"}
    labels = {"openai": "OpenAI m1", "parallel": "Parallel.ai ultra8x", "anthropic": "Anthropic m3"}

    out = format_consolidation(SITE, DX, reports, labels)

    for body in reports.values():
        assert body in out
    for label in labels.values():
        assert f"Report from {label}" in out


def test_consolidation_labels_come_from_the_caller_not_a_hardcoded_map():
    """Attribution must follow the models actually used for the run."""
    out = format_consolidation(
        SITE, DX, {"openai": "R"}, {"openai": "OpenAI custom-model-name"}
    )
    assert "OpenAI custom-model-name" in out


def test_consolidation_falls_back_to_the_key_for_a_missing_label():
    out = format_consolidation(SITE, DX, {"mystery": "R"}, {})
    assert "Report from mystery" in out


def test_consolidation_preserves_report_order():
    reports = {"openai": "AAA", "parallel": "BBB", "anthropic": "CCC"}
    out = format_consolidation(SITE, DX, reports, {})
    assert out.index("AAA") < out.index("BBB") < out.index("CCC")


def test_final_merge_includes_both_consensus_reports():
    out = format_final(SITE, DX, "CONSENSUS_1", "CONSENSUS_2", {"openai": "O", "anthropic": "A"})
    assert "CONSENSUS_1" in out
    assert "CONSENSUS_2" in out
    assert out.index("CONSENSUS_1") < out.index("CONSENSUS_2")


def test_final_merge_uses_phase2_labels():
    """Phase 3 merges Phase 2 output, so it must cite the Phase 2 OpenAI model."""
    cfg = ModelConfig.resolve(openai_phase1="phase1-model", openai_phase2="phase2-model")
    out = format_final(SITE, DX, "C1", "C2", cfg.phase2_labels())
    assert "phase2-model" in out
    assert "phase1-model" not in out


def test_final_merge_demands_references_be_preserved():
    out = format_final(SITE, DX, "C1", "C2", {"openai": "O", "anthropic": "A"})
    assert "reference" in out.lower()


def test_every_prompt_states_the_clinical_context():
    """Site and diagnosis drive the whole point of the tool; none may drop them."""
    labels = {"openai": "O", "parallel": "P", "anthropic": "A"}
    for out in (
        format_phase1(SITE, DX),
        format_consolidation(SITE, DX, {"openai": "R"}, labels),
        format_final(SITE, DX, "C1", "C2", labels),
    ):
        assert SITE in out
        assert DX in out
