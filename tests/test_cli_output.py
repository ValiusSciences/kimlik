"""Guards against rich swallowing bracketed text in user-facing output.

Rich parses `[...]` as markup. An unescaped `[openai]` or `[env: VAR]` is read as
a style tag and silently dropped, so log lines print as "Phase 1  started" with
no provider name and --help loses its env/default hints. This bug shipped twice.
"""

import re
from pathlib import Path

from rich.console import Console

CLI_SOURCE = Path(__file__).resolve().parents[1] / "src" / "kimlik" / "cli.py"


def _render(markup: str) -> str:
    console = Console(file=None, record=True, width=200, no_color=True)
    console.print(markup, end="")
    return console.export_text()


def test_rich_drops_an_unescaped_bracket_word():
    """Documents the failure mode the escaping exists to prevent."""
    assert "openai" not in _render("Phase 1 [openai] started")


def test_escaped_bracket_survives_rendering():
    assert "[openai]" in _render(r"Phase 1 \[openai] started")


def test_escaping_still_allows_real_style_tags():
    assert _render(r"[cyan]Phase 1 \[openai] done[/cyan]").strip() == "Phase 1 [openai] done"


def _console_call_strings(source: str) -> list[str]:
    """Every string literal passed to console.log()/console.print()."""
    return re.findall(r'console\.(?:log|print)\(\s*r?f?"((?:[^"\\]|\\.)*)"', source)


def _strip_interpolations(literal: str) -> str:
    """Drop f-string {...} placeholders.

    Their contents (e.g. ts['output_file']) are Python, evaluated before rich
    ever sees the string, so brackets inside them are not markup.
    """
    return re.sub(r"\{[^{}]*\}", "X", literal)


def test_no_console_call_contains_an_unescaped_non_style_bracket():
    source = CLI_SOURCE.read_text(encoding="utf-8")
    style_tags = {
        "cyan", "green", "red", "yellow", "bold", "/cyan", "/green",
        "/red", "/yellow", "/bold",
    }

    offenders = []
    for literal in _console_call_strings(source):
        # Unescaped '[' is one not preceded by a backslash.
        for tag in re.findall(r"(?<!\\)\[([^\]]*)\]", _strip_interpolations(literal)):
            if tag not in style_tags:
                offenders.append(f"[{tag}]")

    assert not offenders, f"unescaped non-style markup in cli.py: {offenders}"


def test_option_help_strings_escape_their_brackets():
    """--help hints like [env: VAR] and [default: x] must reach the user."""
    source = CLI_SOURCE.read_text(encoding="utf-8")
    for literal in re.findall(r'help=\s*r?f?"((?:[^"\\]|\\.)*)"', source):
        for marker in ("env:", "default:"):
            unescaped = re.search(rf"(?<!\\)\[{marker}", literal)
            assert not unescaped, (
                f"unescaped '[{marker}' in a help string; rich will drop it: {literal!r}"
            )


def test_provider_names_are_present_in_the_rendered_log_lines():
    """End-to-end on the real source: each phase log renders with its provider."""
    source = CLI_SOURCE.read_text(encoding="utf-8")
    literals = [lit for lit in _console_call_strings(source) if "Phase" in lit]
    assert literals, "expected phase log lines in cli.py"

    for literal in literals:
        # Substitute f-string placeholders with a recognisable provider name.
        rendered = _render(re.sub(r"\{[^}]*\}", "openai", literal))
        assert "Phase" in rendered
        if "[" in literal.replace(r"\[", ""):
            continue
        assert "openai" in rendered or "already completed" in rendered
