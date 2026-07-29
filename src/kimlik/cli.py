import asyncio
import os
from datetime import UTC, datetime
from pathlib import Path

import typer
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from kimlik.config import (
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_OPENAI_PHASE1_MODEL,
    DEFAULT_OPENAI_PHASE2_MODEL,
    DEFAULT_PARALLEL_PROCESSOR,
    ModelConfig,
)
from kimlik.prompts import format_consolidation, format_final, format_phase1
from kimlik.providers.anthropic_provider import run_anthropic
from kimlik.providers.openai_provider import (
    PHASE1_MAX_TOKENS,
    PHASE2_MAX_TOKENS,
    get_openai_result,
    run_openai,
    submit_openai_task,
)
from kimlik.providers.parallel_provider import get_parallel_result, submit_parallel_task
from kimlik.state import create_state, load_state, save_state

load_dotenv()

app = typer.Typer(
    help=(
        "Generate tissue- and diagnosis-specific gene signatures "
        "for labeling cell types in scRNA-seq data."
    ),
    add_completion=False,
)
console = Console()

PHASE1_PROVIDERS = ["openai", "parallel", "anthropic"]
PHASE2_PROVIDERS = ["openai", "anthropic"]

# Where to get each credential, shown when one is missing.
REQUIRED_API_KEYS = {
    "OPENAI_API_KEY": "https://platform.openai.com/api-keys",
    "ANTHROPIC_API_KEY": "https://console.anthropic.com/settings/keys",
    "PARALLEL_API_KEY": "https://app.parallel.ai (Settings > API Keys)",
}

# A real report runs tens of thousands of characters. Anything this short means
# the provider produced nothing usable, even though the API call "succeeded":
# the Anthropic tool loop can exhaust its turns, or a response can come back
# with no text blocks at all. Writing that out as a completed report would feed
# an empty file into the next phase with nothing to indicate a problem.
MIN_REPORT_CHARS = 500


def check_api_keys() -> None:
    """Stop before any work starts if credentials are missing.

    Without this the run creates its output directory, submits to all three
    providers, and then reports a bare KeyError once each one fails.
    """
    missing = [name for name in REQUIRED_API_KEYS if not os.environ.get(name)]
    if not missing:
        return

    console.print("[red]Cannot start: missing API key(s).[/red]\n")
    for name in missing:
        console.print(f"  [bold]{name}[/bold]  get one at {REQUIRED_API_KEYS[name]}")

    console.print(
        f"\nkimlik reads keys from a [bold].env[/bold] file in the folder you run it from "
        f"(currently [cyan]{Path.cwd()}[/cyan]), or from your shell environment.\n"
        "\nTo fix, create a file named [bold].env[/bold] here containing:\n"
    )
    for name in REQUIRED_API_KEYS:
        console.print(f"  {name}=your-key-here")
    console.print("\nAll three providers are required for a run.")
    raise typer.Exit(1)


def format_duration(seconds: float) -> str:
    """Render a span the way someone reading a terminal wants to see it."""
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m {seconds % 60:02d}s"
    return f"{seconds // 3600}h {(seconds % 3600) // 60:02d}m"


def task_duration(task: dict) -> str:
    """How long one provider took, or '-' if it never ran to completion."""
    started, completed = task.get("started_at"), task.get("completed_at")
    if not started or not completed:
        return "-"
    try:
        elapsed = (
            datetime.fromisoformat(completed) - datetime.fromisoformat(started)
        ).total_seconds()
    except ValueError:
        return "-"
    return format_duration(elapsed) if elapsed >= 0 else "-"


def wall_clock(state: dict) -> str:
    """Total elapsed time across the run.

    Phase 1 providers run concurrently, so this is the span from the first
    start to the last finish, not the sum of the parts.
    """
    starts, ends = [], []
    for phase in ("phase1", "phase2", "phase3"):
        for task in state.get(phase, {}).values():
            if task.get("started_at"):
                starts.append(datetime.fromisoformat(task["started_at"]))
            if task.get("completed_at"):
                ends.append(datetime.fromisoformat(task["completed_at"]))
    if not starts or not ends:
        return "-"
    return format_duration((max(ends) - min(starts)).total_seconds())


def write_report(output_dir: Path, filename: str, content: str, label: str) -> str:
    """Write a provider's report, refusing to accept an empty or stunted one."""
    stripped = content.strip()
    if not stripped:
        raise RuntimeError(
            f"{label} returned an empty report. Nothing was written. "
            "Re-run to retry; completed providers are skipped."
        )
    if len(stripped) < MIN_REPORT_CHARS:
        raise RuntimeError(
            f"{label} returned only {len(stripped)} characters, far short of a usable "
            f"report (expected at least {MIN_REPORT_CHARS}). Treating this as a failure "
            "rather than passing it to the next phase. Re-run to retry."
        )
    (output_dir / filename).write_text(content, encoding="utf-8")
    return filename


# ---------------------------------------------------------------------------
# Phase 1 helpers
# ---------------------------------------------------------------------------


async def _run_phase1_provider(
    name: str,
    state: dict,
    output_dir: Path,
    lock: asyncio.Lock,
    prompt: str,
    models: ModelConfig,
) -> None:
    ts = state["phase1"][name]

    async with lock:
        ts["status"] = "running"
        ts["started_at"] = datetime.now(UTC).isoformat()
        save_state(output_dir, state)

    console.log(rf"[cyan]Phase 1 \[{name}] started[/cyan]")

    try:
        if name == "openai":
            if not ts.get("task_id"):
                response_id = await submit_openai_task(
                    prompt, models.openai_phase1, PHASE1_MAX_TOKENS
                )
                async with lock:
                    ts["task_id"] = response_id
                    save_state(output_dir, state)
                console.log(
                    rf"[cyan]Phase 1 \[openai] submitted → response_id={response_id}[/cyan]"
                )
            else:
                response_id = ts["task_id"]
                console.log(rf"[cyan]Phase 1 \[openai] resuming response_id={response_id}[/cyan]")
            content = await get_openai_result(response_id)

        elif name == "parallel":
            loop = asyncio.get_event_loop()

            if not ts.get("task_id"):
                # Fresh submission — save run_id immediately so we can resume on crash.
                run_id = await loop.run_in_executor(
                    None, submit_parallel_task, prompt, models.parallel_processor
                )
                async with lock:
                    ts["task_id"] = run_id
                    save_state(output_dir, state)
                console.log(rf"[cyan]Phase 1 \[parallel] submitted → run_id={run_id}[/cyan]")
            else:
                run_id = ts["task_id"]
                console.log(rf"[cyan]Phase 1 \[parallel] resuming run_id={run_id}[/cyan]")

            content = await loop.run_in_executor(None, get_parallel_result, run_id)

        elif name == "anthropic":
            content = await run_anthropic(prompt, models.anthropic, use_tools=True)

        else:
            raise ValueError(f"Unknown provider: {name}")

        output_file = write_report(
            output_dir, f"phase1_{name}.md", content, f"Phase 1 [{name}]"
        )

        async with lock:
            ts["status"] = "completed"
            ts["output_file"] = output_file
            ts["completed_at"] = datetime.now(UTC).isoformat()
            ts["error"] = None
            save_state(output_dir, state)

        console.log(rf"[green]Phase 1 \[{name}] done → {output_file}[/green]")

    except Exception as exc:
        async with lock:
            ts["status"] = "failed"
            ts["error"] = str(exc)
            ts["completed_at"] = datetime.now(UTC).isoformat()
            save_state(output_dir, state)
        console.log(rf"[red]Phase 1 \[{name}] failed: {exc}[/red]")
        raise


# ---------------------------------------------------------------------------
# Phase 2 helpers
# ---------------------------------------------------------------------------


async def _run_phase2_provider(
    name: str,
    state: dict,
    output_dir: Path,
    lock: asyncio.Lock,
    prompt: str,
    models: ModelConfig,
) -> None:
    ts = state["phase2"][name]

    async with lock:
        ts["status"] = "running"
        ts["started_at"] = datetime.now(UTC).isoformat()
        save_state(output_dir, state)

    console.log(rf"[cyan]Phase 2 \[{name}] consolidation started[/cyan]")

    try:
        if name == "openai":
            content = await run_openai(prompt, models.openai_phase2, PHASE2_MAX_TOKENS)
        elif name == "anthropic":
            content = await run_anthropic(prompt, models.anthropic, use_tools=False)
        else:
            raise ValueError(f"Unknown phase-2 provider: {name}")

        output_file = write_report(
            output_dir, f"phase2_{name}_consensus.md", content, f"Phase 2 [{name}]"
        )

        async with lock:
            ts["status"] = "completed"
            ts["output_file"] = output_file
            ts["completed_at"] = datetime.now(UTC).isoformat()
            ts["error"] = None
            save_state(output_dir, state)

        console.log(rf"[green]Phase 2 \[{name}] done → {output_file}[/green]")

    except Exception as exc:
        async with lock:
            ts["status"] = "failed"
            ts["error"] = str(exc)
            ts["completed_at"] = datetime.now(UTC).isoformat()
            save_state(output_dir, state)
        console.log(rf"[red]Phase 2 \[{name}] failed: {exc}[/red]")
        raise


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


async def run_pipeline(
    biopsy_site: str,
    tumor_diagnosis: str,
    output_dir: Path,
    force: bool,
    models: ModelConfig,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    console.print(
        "[bold]Models:[/bold] "
        f"phase1 openai=[cyan]{models.openai_phase1}[/cyan] "
        f"parallel=[cyan]{models.parallel_processor}[/cyan] "
        f"anthropic=[cyan]{models.anthropic}[/cyan] | "
        f"phase2 openai=[cyan]{models.openai_phase2}[/cyan]"
    )

    # Load or initialise state
    state = None if force else load_state(output_dir)

    if state is None:
        state = create_state(biopsy_site, tumor_diagnosis, str(output_dir), models.as_dict())
        save_state(output_dir, state)
        console.print(f"[bold]New run[/bold] → [cyan]{output_dir}[/cyan]")
    else:
        if (
            state["biopsy_site"] != biopsy_site
            or state["tumor_diagnosis"] != tumor_diagnosis
        ):
            console.print(
                "[yellow]WARNING: existing state has different parameters.[/yellow]\n"
                f"  State:   biopsy_site={state['biopsy_site']!r}\n"
                f"           tumor_diagnosis={state['tumor_diagnosis']!r}\n"
                f"  Current: biopsy_site={biopsy_site!r}\n"
                f"           tumor_diagnosis={tumor_diagnosis!r}\n"
                "Pass --force to restart with the new parameters."
            )
            raise typer.Exit(1)
        console.print(f"[bold]Resuming[/bold] from [cyan]{output_dir}[/cyan]")

        # Changing models mid-run is allowed (e.g. retrying a failed provider on a
        # different model), but the state file should not keep claiming the old ones.
        recorded = state.get("models") or {}
        if recorded and recorded != models.as_dict():
            console.print(
                "[yellow]NOTE: models differ from the recorded run.[/yellow]\n"
                f"  Recorded: {recorded}\n"
                f"  Current:  {models.as_dict()}\n"
                "Already-completed outputs keep whichever model produced them."
            )
        state["models"] = models.as_dict()
        save_state(output_dir, state)

    lock = asyncio.Lock()

    # ---- Phase 1 --------------------------------------------------------
    console.rule("[bold]Phase 1: independent reports[/bold]")
    phase1_prompt = format_phase1(biopsy_site, tumor_diagnosis)

    tasks = []
    for name in PHASE1_PROVIDERS:
        ts = state["phase1"][name]
        if ts["status"] == "completed":
            console.print(
                rf"  Phase 1 \[{name}]: already completed ({ts['output_file']}), skipping."
            )
        else:
            if ts["status"] == "failed":
                # Reset so we retry cleanly
                ts["status"] = "pending"
                ts["error"] = None
            tasks.append(
                asyncio.create_task(
                    _run_phase1_provider(name, state, output_dir, lock, phase1_prompt, models),
                    name=f"phase1-{name}",
                )
            )

    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        failures = [r for r in results if isinstance(r, BaseException)]
        if failures:
            console.print(
                f"[red]{len(failures)} Phase 1 provider(s) failed. "
                "Fix the error and re-run; completed providers will be skipped.[/red]"
            )
            raise typer.Exit(1)

    # Reload state (tasks write it concurrently)
    state = load_state(output_dir)

    still_pending = [
        n for n in PHASE1_PROVIDERS if state["phase1"][n]["status"] != "completed"
    ]
    if still_pending:
        console.print(f"[red]Phase 1 incomplete for: {still_pending}[/red]")
        raise typer.Exit(1)

    # ---- Phase 2 --------------------------------------------------------
    console.rule("[bold]Phase 2: consolidation[/bold]")

    phase1_outputs: dict[str, str] = {}
    for name in PHASE1_PROVIDERS:
        ts = state["phase1"][name]
        phase1_outputs[name] = (output_dir / ts["output_file"]).read_text(encoding="utf-8")

    consolidation_prompt = format_consolidation(
        biopsy_site, tumor_diagnosis, phase1_outputs, models.phase1_labels()
    )

    tasks = []
    for name in PHASE2_PROVIDERS:
        ts = state["phase2"][name]
        if ts["status"] == "completed":
            console.print(
                rf"  Phase 2 \[{name}]: already completed ({ts['output_file']}), skipping."
            )
        else:
            if ts["status"] == "failed":
                ts["status"] = "pending"
                ts["error"] = None
            tasks.append(
                asyncio.create_task(
                    _run_phase2_provider(
                        name, state, output_dir, lock, consolidation_prompt, models
                    ),
                    name=f"phase2-{name}",
                )
            )

    if tasks:
        results = await asyncio.gather(*tasks, return_exceptions=True)
        failures = [r for r in results if isinstance(r, BaseException)]
        if failures:
            console.print(
                f"[red]{len(failures)} Phase 2 provider(s) failed. "
                "Re-run to retry; Phase 1 results are cached.[/red]"
            )

    state = load_state(output_dir)

    still_pending = [
        n for n in PHASE2_PROVIDERS if state["phase2"][n]["status"] != "completed"
    ]
    if still_pending:
        console.print(f"[red]Phase 2 incomplete for: {still_pending}[/red]")
        raise typer.Exit(1)

    # ---- Phase 3 — final merge ------------------------------------------
    console.rule("[bold]Phase 3: final merge[/bold]")

    ts3 = state["phase3"]["anthropic"]
    if ts3["status"] == "completed":
        console.print(f"  Phase 3: already completed ({ts3['output_file']}), skipping.")
    else:
        if ts3["status"] == "failed":
            ts3["status"] = "pending"
            ts3["error"] = None

        openai_consensus = (
            output_dir / state["phase2"]["openai"]["output_file"]
        ).read_text(encoding="utf-8")
        anthropic_consensus = (
            output_dir / state["phase2"]["anthropic"]["output_file"]
        ).read_text(encoding="utf-8")
        final_prompt = format_final(
            biopsy_site,
            tumor_diagnosis,
            openai_consensus,
            anthropic_consensus,
            models.phase2_labels(),
        )

        async with lock:
            ts3["status"] = "running"
            ts3["started_at"] = datetime.now(UTC).isoformat()
            save_state(output_dir, state)

        console.log(r"[cyan]Phase 3 \[anthropic] final merge started[/cyan]")
        try:
            content = await run_anthropic(final_prompt, models.anthropic, use_tools=False)
            output_file = write_report(
                output_dir, "phase3_final.md", content, "Phase 3 [anthropic]"
            )

            async with lock:
                ts3["status"] = "completed"
                ts3["output_file"] = output_file
                ts3["completed_at"] = datetime.now(UTC).isoformat()
                ts3["error"] = None
                save_state(output_dir, state)

            console.log(rf"[green]Phase 3 \[anthropic] done → {output_file}[/green]")
        except Exception as exc:
            async with lock:
                ts3["status"] = "failed"
                ts3["error"] = str(exc)
                ts3["completed_at"] = datetime.now(UTC).isoformat()
                save_state(output_dir, state)
            console.log(rf"[red]Phase 3 \[anthropic] failed: {exc}[/red]")
            raise typer.Exit(1) from exc

    # ---- Summary --------------------------------------------------------
    state = load_state(output_dir)
    console.rule("[bold]Summary[/bold]")

    table = Table()
    table.add_column("Phase", style="bold")
    table.add_column("Provider")
    table.add_column("Status")
    table.add_column("Duration", justify="right")
    table.add_column("Output file")
    table.add_column("Error")

    for phase_key, providers in [
        ("phase1", PHASE1_PROVIDERS),
        ("phase2", PHASE2_PROVIDERS),
        ("phase3", ["anthropic"]),
    ]:
        label = {"phase1": "Phase 1", "phase2": "Phase 2", "phase3": "Phase 3"}[phase_key]
        for prov in providers:
            ts = state[phase_key][prov]
            ok = ts["status"] == "completed"
            status_str = f"[green]{ts['status']}[/green]" if ok else f"[red]{ts['status']}[/red]"
            table.add_row(
                label,
                prov,
                status_str,
                task_duration(ts),
                ts.get("output_file") or "-",
                ts.get("error") or "",
            )

    console.print(table)
    console.print(
        f"Total wall time: [bold]{wall_clock(state)}[/bold] "
        "(Phase 1 providers run concurrently, so this is less than the sum above)."
    )


# ---------------------------------------------------------------------------
# CLI entrypoint
# ---------------------------------------------------------------------------


@app.command()
def main(
    biopsy_site: str = typer.Option(
        ...,
        "--biopsy-site",
        "-b",
        help="Biopsy site, e.g. 'right lung'",
    ),
    tumor_diagnosis: str = typer.Option(
        ...,
        "--tumor-diagnosis",
        "-t",
        help="Tumor diagnosis, e.g. 'metastatic osteosarcoma (primary: distal femur)'",
    ),
    output_dir: Path = typer.Option(
        Path("./kimlik_output"),
        "--output-dir",
        "-o",
        help="Directory for outputs and state file",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Ignore existing state and start a fresh run",
    ),
    openai_phase1_model: str = typer.Option(
        None,
        "--openai-phase1-model",
        help=(
            rf"OpenAI model for Phase 1 research "
            rf"\[env: KIMLIK_OPENAI_PHASE1_MODEL] \[default: {DEFAULT_OPENAI_PHASE1_MODEL}]"
        ),
    ),
    openai_phase2_model: str = typer.Option(
        None,
        "--openai-phase2-model",
        help=(
            rf"OpenAI model for Phase 2 consolidation "
            rf"\[env: KIMLIK_OPENAI_PHASE2_MODEL] \[default: {DEFAULT_OPENAI_PHASE2_MODEL}]"
        ),
    ),
    anthropic_model: str = typer.Option(
        None,
        "--anthropic-model",
        help=(
            rf"Anthropic model for all phases "
            rf"\[env: KIMLIK_ANTHROPIC_MODEL] \[default: {DEFAULT_ANTHROPIC_MODEL}]"
        ),
    ),
    parallel_processor: str = typer.Option(
        None,
        "--parallel-processor",
        help=(
            rf"Parallel.ai processor "
            rf"\[env: KIMLIK_PARALLEL_PROCESSOR] \[default: {DEFAULT_PARALLEL_PROCESSOR}]"
        ),
    ),
) -> None:
    check_api_keys()
    models = ModelConfig.resolve(
        openai_phase1=openai_phase1_model,
        openai_phase2=openai_phase2_model,
        anthropic=anthropic_model,
        parallel_processor=parallel_processor,
    )
    asyncio.run(run_pipeline(biopsy_site, tumor_diagnosis, output_dir, force, models))


if __name__ == "__main__":
    app()
