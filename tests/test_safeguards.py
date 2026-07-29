"""Guards against a run that appears to succeed while producing nothing usable."""

import pytest
import typer

from kimlik.cli import MIN_REPORT_CHARS, REQUIRED_API_KEYS, check_api_keys, write_report

GOOD_REPORT = "# Report\n\n" + ("marker gene tables and references. " * 40)


@pytest.fixture
def all_keys_set(monkeypatch):
    for name in REQUIRED_API_KEYS:
        monkeypatch.setenv(name, "test-key")


# ---------------------------------------------------------------------------
# Empty / stunted report rejection
# ---------------------------------------------------------------------------


def test_a_real_report_is_written(tmp_path):
    assert len(GOOD_REPORT) > MIN_REPORT_CHARS
    name = write_report(tmp_path, "phase1_openai.md", GOOD_REPORT, "Phase 1 [openai]")
    assert (tmp_path / name).read_text() == GOOD_REPORT


@pytest.mark.parametrize("content", ["", "   ", "\n\n\t "])
def test_empty_report_raises_instead_of_being_saved(tmp_path, content):
    """Regression: the Anthropic tool loop can exhaust its turns and return "",
    which used to be written out and marked completed."""
    with pytest.raises(RuntimeError, match="empty report"):
        write_report(tmp_path, "phase1_anthropic.md", content, "Phase 1 [anthropic]")
    assert list(tmp_path.iterdir()) == []


def test_stunted_report_raises_instead_of_being_saved(tmp_path):
    with pytest.raises(RuntimeError, match="far short of a usable report"):
        write_report(tmp_path, "phase1_anthropic.md", "too short", "Phase 1 [anthropic]")
    assert list(tmp_path.iterdir()) == []


def test_rejected_report_never_reaches_disk(tmp_path):
    """A partial file on disk would be consumed by the next phase."""
    with pytest.raises(RuntimeError):
        write_report(tmp_path, "phase2_openai_consensus.md", "x", "Phase 2 [openai]")
    assert not (tmp_path / "phase2_openai_consensus.md").exists()


def test_failure_message_names_the_phase_and_provider(tmp_path):
    with pytest.raises(RuntimeError, match=r"Phase 1 \[anthropic\]"):
        write_report(tmp_path, "phase1_anthropic.md", "", "Phase 1 [anthropic]")


def test_report_is_written_verbatim(tmp_path):
    """No normalisation: references and trailing content must survive intact."""
    body = GOOD_REPORT + "\n\n1. Zhou Y, et al. Nature Communications. 2020;11:6322.\n"
    name = write_report(tmp_path, "phase3_final.md", body, "Phase 3 [anthropic]")
    assert (tmp_path / name).read_text() == body


# ---------------------------------------------------------------------------
# Pre-flight API key check
# ---------------------------------------------------------------------------


def test_passes_when_every_key_is_present(all_keys_set):
    check_api_keys()  # must not raise


@pytest.mark.parametrize("missing", sorted(REQUIRED_API_KEYS))
def test_exits_when_a_key_is_missing(all_keys_set, monkeypatch, capsys, missing):
    monkeypatch.delenv(missing)
    with pytest.raises(typer.Exit):
        check_api_keys()
    assert missing in capsys.readouterr().out


def test_empty_string_key_counts_as_missing(all_keys_set, monkeypatch):
    """A blank line in .env sets the variable to "" and would otherwise pass."""
    monkeypatch.setenv("OPENAI_API_KEY", "")
    with pytest.raises(typer.Exit):
        check_api_keys()


def test_error_names_every_missing_key_at_once(monkeypatch, capsys):
    """Fixing one key at a time across three runs is a miserable first experience."""
    for name in REQUIRED_API_KEYS:
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(typer.Exit):
        check_api_keys()
    out = capsys.readouterr().out
    for name in REQUIRED_API_KEYS:
        assert name in out


def test_error_explains_how_to_fix_it(monkeypatch, capsys):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(typer.Exit):
        check_api_keys()
    out = capsys.readouterr().out
    assert ".env" in out                                  # where keys go
    assert "platform.openai.com" in out                   # where to get one
    assert "your-key-here" in out                         # the shape of the file


def test_check_runs_before_any_output_directory_is_created(monkeypatch, tmp_path):
    """The old behaviour created a directory and fired all three providers first."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    with pytest.raises(typer.Exit):
        check_api_keys()
    assert list(tmp_path.iterdir()) == []
