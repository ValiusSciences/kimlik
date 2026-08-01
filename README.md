# kimlik

[![CI](https://github.com/ValiusSciences/kimlik/workflows/CI/badge.svg)](https://github.com/ValiusSciences/kimlik/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Research use only](https://img.shields.io/badge/use-research%20only-important.svg)](#data-and-privacy)

**Tissue- and diagnosis-specific gene signatures for labeling cell types in single-cell RNA-seq data.**

`kimlik` (Turkish for *identity*) is a command-line tool that generates a consensus gene-signature report for annotating scRNA-seq data, tailored to a specific biopsy site and tumor diagnosis. Instead of reaching for a generic marker panel, you get a literature-backed reference for the tissue and disease context you are actually working in.

It queries three LLM providers in parallel, has two of them independently consolidate the results, then merges those into a single definitive guide, with citations to peer-reviewed literature at every step.

## Read the example before you install anything

A complete run is committed to this repository. Open **[`results/example-osteosarcoma-lung-met/phase3_final.md`](results/example-osteosarcoma-lung-met/phase3_final.md)** and read it in your browser right now. It costs nothing, needs no setup, and shows exactly what the tool produces.

It is a lung biopsy of metastatic osteosarcoma. Here is a fragment:

| Cell type | Core markers | Notes | Refs |
|---|---|---|---|
| **Lung epithelium** | `EPCAM, KRT8, KRT18, KRT19, CDH1` | Surfactant RNA is often ambient; require coherent co-expression | [52-57] |
| **Mesothelium (pleura)** | `MSLN, UPK3B, WT1, CALB2, ITLN1` | Common in pleural-based biopsies; frequently misannotated | [52, 53, 65] |
| **Skeletal myocyte / myoblast** | `MYL1, MYLPF, TNNT1, ACTA1, MYOD1` | Discrete cluster in limb osteosarcoma; **should be absent in lung** | [1] |
| **Cycling (any lineage)** | `MKI67, TOP2A, CCNB1, CENPF, PCNA` | Annotate as "cycling (parent lineage)", never as its own type | [118] |

The full guide is 82 KB across 17 sections with 145 references, including a copy-paste marker dictionary for R and Seurat. If it looks useful, the rest of this README walks you through running your own.

## Why site-specific panels matter

For a primary tumor, a stock tissue panel usually gets you most of the way. The problem appears once disease spreads, because **a metastatic biopsy contains cells that do not belong to the tissue it was taken from.**

Take osteosarcoma that has metastasized to lung, the example shipped in this repo. That biopsy holds three populations at once:

- **Lung parenchyma and stroma** native to the biopsy site: AT1/AT2 pneumocytes, club and ciliated cells, alveolar macrophages.
- **Osteoblastic tumor cells** carrying their bone lineage program (`RUNX2`, `SP7`, `COL1A1`, `ALPL`, `IBSP`), sitting in tissue where no bone markers belong.
- **A tumor microenvironment** shaped by both.

A generic lung panel silently mislabels the tumor compartment; a generic bone panel misses the microenvironment. `kimlik` is built for exactly this case: you give it both the site *and* the diagnosis, and the report covers the resident tissue, the metastatic tumor lineage, and the immune and stromal compartments together.

## What you need before you start
**1. Accounts at three AI providers, each with billing enabled.** kimlik deliberately asks three independent providers the same question and cross-checks their answers, so all three are required. There is no single-provider mode.

| Provider | Sign up | Where to get your key |
|---|---|---|
| OpenAI | https://platform.openai.com | https://platform.openai.com/api-keys |
| Anthropic | https://console.anthropic.com | https://console.anthropic.com/settings/keys |
| Parallel.ai | https://app.parallel.ai | https://app.parallel.ai then Settings > API Keys |


**2. About an hour of waiting.** A run takes roughly 45 to 60 minutes, most of it spent waiting on deep literature research. You do not need to watch it. You do need to leave the terminal window open, though an interrupted run can be resumed.

**4. Money.** You pay the three providers directly for the tokens the run consumes. The example run in this repo produced 316 KB of reports, roughly 80,000 output tokens across six model calls, plus about 90,000 tokens of input for the consolidation and merge steps. The example run costs about $15 OpenAI credits, about $15 Antrhopic credits, $5 Parallel.ai credits.

Provider rates change often, so rather than print figures here that quietly go stale, check them against the footprint above:

| Provider | Pricing |
|---|---|
| OpenAI | https://openai.com/api/pricing/ |
| Anthropic | https://www.anthropic.com/pricing |
| Parallel.ai | https://docs.parallel.ai |

To spend less, drop to a cheaper research processor and a smaller reasoning model (see [Choosing models](#choosing-models)):

```bash
kimlik -b "..." -t "..." --parallel-processor ultra4x --openai-phase1-model gpt-5.5
```


## Installing

### Step 1: install uv

[uv](https://docs.astral.sh/uv/) is a single tool that manages the Python version, the virtual environment, and the packages. Using it means you do not have to think about any of those. Paste one line into your terminal:

```bash
# macOS or Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```powershell
# Windows PowerShell
winget install astral-sh.uv
```

Close and reopen your terminal, then confirm it worked:

```bash
uv --version
```

You should see a version number. If you instead see "command not found", reopening the terminal usually fixes it, because the installer edits your shell configuration.

### Step 2: download kimlik

```bash
git clone https://github.com/ValiusSciences/kimlik.git
cd kimlik
```

If `git` is not installed, you can instead download the repository as a ZIP from the green "Code" button on the GitHub page, unzip it, and `cd` into the unzipped folder.

### Step 3: install it

```bash
uv sync
```

This creates a self-contained environment inside the folder and installs the `kimlik` command into it. Nothing is installed system-wide, and deleting the folder removes everything.

Confirm it worked:

```bash
uv run kimlik --help
```

You should see the list of options. Note the `uv run` prefix: it tells uv to use the environment it just built. Every command below uses it.

### Alternative: install with pip

If you already manage Python yourself and would rather not add uv:

```bash
git clone https://github.com/ValiusSciences/kimlik.git
cd kimlik

python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

pip install .
kimlik --help
```

With this route you activate the environment yourself and call `kimlik` directly, without the `uv run` prefix.

## Setting up your API keys

kimlik reads your three keys from a file named `.env`. Create it by copying the template:

```bash
cp .env.example .env
```

Then open `.env` in any text editor and paste your keys in, replacing the placeholder after each `=` sign:

```dotenv
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PARALLEL_API_KEY=...
```

Save the file. There are no quotes and no spaces around the `=`. The tool loads this file automatically every time it starts.

`.env` is listed in `.gitignore`, so it will never be committed to version control. Keep it that way.

**Two alternatives**, if you prefer not to use a file. Set them in your shell for the session:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export PARALLEL_API_KEY="..."
```

Or supply them inline for a single run:

```bash
OPENAI_API_KEY="sk-..." ANTHROPIC_API_KEY="sk-ant-..." PARALLEL_API_KEY="..." \
  kimlik --biopsy-site "..." --tumor-diagnosis "..."
```

kimlik checks all three keys before it does any billable work, and if one is missing it tells you which one and where to get it.

## Running your first report

```bash
uv run kimlik \
  --biopsy-site "right lung" \
  --tumor-diagnosis "metastatic osteosarcoma (primary: distal femur)" \
  --output-dir ./my_run
```

The backslashes let one command span several lines. You can also write it on a single line and leave them out.

Three things to fill in:

| What you write | What it means |
|---|---|
| `--biopsy-site "right lung"` | Where the tissue came from. Plain clinical language. |
| `--tumor-diagnosis "metastatic osteosarcoma (primary: distal femur)"` | The diagnosis. Include the primary site for a metastasis, since that is what lets the report separate tumor from resident tissue. |
| `--output-dir ./my_run` | A new folder for the results. Pick a fresh name per case. |

Each option has a short form, so the same command reads:

```bash
uv run kimlik -b "right lung" -t "metastatic osteosarcoma (primary: distal femur)" -o ./my_run
```

**Do not put patient identifiers in either field.** Both are sent to third-party APIs as prompt text. See [Data and privacy](#data-and-privacy).

## What to expect while it runs

kimlik prints the models it is about to use, then works through three phases. Output looks like this:

```
Models: phase1 openai=gpt-5.5-pro parallel=ultra8x anthropic=claude-opus-5 | phase2 openai=gpt-5.5
New run -> ./my_run
───────────────────────── Phase 1: independent reports ─────────────────────────
[09:26:17] Phase 1 [openai] started
           Phase 1 [parallel] started
           Phase 1 [anthropic] started
           Phase 1 [parallel] submitted -> run_id=trun_a2d3...
           Phase 1 [openai] submitted -> response_id=resp_0d9f...
  searching literature (round 3/30): osteosarcoma single-cell RNA-seq markers
  Parallel.ai still researching: 15 min elapsed, will keep waiting up to 105 more min.
  OpenAI still working: 10 min elapsed.
           Phase 1 [anthropic] done -> phase1_anthropic.md
           Phase 1 [openai] done -> phase1_openai.md
           Phase 1 [parallel] done -> phase1_parallel.md
────────────────────────────── Phase 2: consolidation ──────────────────────────
...
```

**Long silences are normal and expected.** Deep research runs for tens of minutes with nothing to report. Every long wait prints a heartbeat every 5 minutes so you can tell the difference between working and frozen. If you are seeing heartbeats, leave it alone.

Roughly how the hour is spent, measured on the example case:

| Stage | Measured | Notes |
|---|---|---|
| Phase 1, Parallel.ai `ultra8x` | 30 - 44 min | Deep multi-source research; the long pole |
| Phase 1, OpenAI `gpt-5.5-pro` | 12 - 14 min | Reasoning model; varies with output length |
| Phase 1, Anthropic `claude-opus-5` | 8 - 9 min | Agentic loop; ran 15 PubMed searches in one run |
| Phase 2, Anthropic | 8 min | Starts once all Phase 1 outputs are ready |
| Phase 2, OpenAI | 3 - 4 min | Runs concurrently with Phase 2 Anthropic |
| Phase 3, final merge | 7 - 9 min | Starts once both Phase 2 reports are ready |
| **Total wall clock** | **about 47 min** | Uninterrupted run, defaults, all three providers |

The three Phase 1 providers run **concurrently**, so the total is set by the slowest one rather than the sum. Your times will vary with the tumor type and how much literature exists for it, but the shape holds: Parallel.ai sets the pace.

At the end you get a summary table showing every provider, whether it succeeded, how long it took, and which file it wrote.

**If you need to stop it**, press Ctrl+C. Nothing finished is lost. Re-run the exact same command and it picks up where it left off without repaying for completed work.

The 2-hour figure mentioned elsewhere in this README is the built-in timeout, not an expectation.

## What you get at the end

Your output folder contains seven files:

```
my_run/
├── phase3_final.md               # READ THIS ONE. The single merged guide.
├── phase1_openai.md              # OpenAI's independent report
├── phase1_parallel.md            # Parallel.ai's deep-research report
├── phase1_anthropic.md           # Anthropic's report (PubMed + web search)
├── phase2_openai_consensus.md    # OpenAI's consensus of all 3 reports
├── phase2_anthropic_consensus.md # Anthropic's consensus of all 3 reports
└── kimlik_state.json             # run bookkeeping (do not delete while running)
```

Start with `phase3_final.md` and ignore the rest unless you want to audit how the three literature searches converged, and where they disagreed.

These are plain Markdown text files. You can open one in any text editor, but it is much easier to read rendered: drag it into a Markdown viewer, open it in VS Code and press Cmd/Ctrl+Shift+V, or just push it to a GitHub repository or Gist, which renders Markdown automatically.

## The example output in detail

Everything under [`results/example-osteosarcoma-lung-met/`](results/example-osteosarcoma-lung-met/) came from this one command:

```bash
kimlik \
  -b "right lung" \
  -t "metastatic osteosarcoma (primary: distal femur)" \
  -o results/example-osteosarcoma-lung-met
```

| File | Size | Produced by |
|---|---|---|
| `phase1_openai.md` | 35 KB | OpenAI `gpt-5.5-pro` |
| `phase1_parallel.md` | 32 KB | Parallel.ai `ultra8x` (44 min) |
| `phase1_anthropic.md` | 49 KB | Anthropic `claude-opus-5` + PubMed/web search |
| `phase2_openai_consensus.md` | 42 KB | OpenAI `gpt-5.5` |
| `phase2_anthropic_consensus.md` | 76 KB | Anthropic `claude-opus-5` |
| `phase3_final.md` | 82 KB | Anthropic `claude-opus-5` |

The structure of the final guide is the argument for the tool. Alongside the malignant osteosarcoma compartment (`RUNX2`, `SP7`, `COL1A1`, `ALPL`, `IBSP`) and the resident lung epithelium (`SFTPC`, `AGER`, `SCGB1A1`, `FOXJ1`), it devotes whole sections to *high-priority marker-collision warnings* (10) and *expected cluster composition for this specimen* (11), and a subsection to the *epithelial-malignancy differentials* a lung biopsy forces you to exclude (6.3). Those exist only because the site and the diagnosis disagree, and a generic panel would give you none of them. Section 13 is a copy-paste R/Seurat signature dictionary.

Two things to notice, because they are what you should expect from your own runs rather than flaws in this one:

- **Every in-text citation resolves.** The guide cites up to `[144]` against 145 listed references, with no dangling numbers. That is the property most at risk when a long report gets truncated, so it is worth checking on your own output.
- **25 of the 145 references carry an `[unverified]` flag.** The models mark citations they could not confirm against a source rather than presenting everything with equal confidence. Verify flagged references yourself before relying on them.

This is the only run committed to the repository. Everything else under `results/` is gitignored by default, so real cases cannot be pushed by accident.

## How it works

```
Phase 1 (parallel)
├── OpenAI gpt-5.5-pro        -> phase1_openai.md
├── Parallel.ai ultra8x       -> phase1_parallel.md
└── Anthropic claude-opus-5   -> phase1_anthropic.md
        (web search + PubMed tools enabled)

Phase 2 (parallel consolidation; receives all 3 Phase 1 reports as context)
├── OpenAI gpt-5.5            -> phase2_openai_consensus.md
└── Anthropic claude-opus-5   -> phase2_anthropic_consensus.md

Phase 3 (final merge; receives both Phase 2 reports as context)
└── Anthropic claude-opus-5   -> phase3_final.md
```

Three separate searches, two separate consolidations, one merge. A marker only one provider proposes stays visible as such in the Phase 1 files, which is the reason all six intermediate reports are kept rather than discarded.

**What agreement between providers does and does not tell you.** Three models querying overlapping literature, and in places overlapping training data, are not three independent observers. Convergence here means the claim is well represented in the accessible literature, not that it has been independently replicated. Treat it as a way to surface and localise disagreement, not as evidence in its own right, and read the primary citation before acting on any marker.

## Data and privacy

**Do not pass protected health information to this tool.**

`kimlik` takes only two inputs, a biopsy site and a tumor diagnosis, and both are transmitted to third-party LLM APIs (OpenAI, Anthropic, Parallel.ai) as prompt text. Keep them at the level of clinical description (`"right lung"`, `"metastatic osteosarcoma"`). Never include names, medical record numbers, dates of birth, accession numbers, or any other identifier.

The tool never reads your expression matrices, count files, or any patient-level data. Its outputs are literature-derived marker panels containing no patient information, but if you organize output directories by case, treat those directories as you would any other study artifact and keep them out of version control. `results/` is gitignored for exactly this reason.

**Research use only. Not a diagnostic device.** These panels are literature summaries generated by language models. Clinically consequential cell-identity calls must be corroborated by histopathology, IHC, and, where indicated, orthogonal molecular testing.

## All options

```
Options:
  -b, --biopsy-site TEXT        Biopsy site, e.g. 'right lung'  [required]
  -t, --tumor-diagnosis TEXT    Tumor diagnosis, e.g. 'metastatic osteosarcoma'  [required]
  -o, --output-dir PATH         Output directory (default: ./kimlik_output)
  -f, --force                   Ignore existing state and start a fresh run
  --openai-phase1-model TEXT    OpenAI model for Phase 1 research
  --openai-phase2-model TEXT    OpenAI model for Phase 2 consolidation
  --anthropic-model TEXT        Anthropic model for all phases
  --parallel-processor TEXT     Parallel.ai processor
  --help                        Show this message and exit.
```

### Choosing models

Model names change faster than this tool does, so every model is overridable. You should never need to edit source to move to a newer generation. Each setting resolves in this order: **CLI flag, then environment variable, then built-in default.**

| Setting | CLI flag | Environment variable | Default |
|---|---|---|---|
| Phase 1 research (OpenAI) | `--openai-phase1-model` | `KIMLIK_OPENAI_PHASE1_MODEL` | `gpt-5.5-pro` |
| Phase 2 consolidation (OpenAI) | `--openai-phase2-model` | `KIMLIK_OPENAI_PHASE2_MODEL` | `gpt-5.5` |
| All Anthropic phases | `--anthropic-model` | `KIMLIK_ANTHROPIC_MODEL` | `claude-opus-5` |
| Parallel.ai processor | `--parallel-processor` | `KIMLIK_PARALLEL_PROCESSOR` | `ultra8x` |

Per-run override:

```bash
kimlik -b "right lung" -t "metastatic osteosarcoma" \
  --anthropic-model claude-opus-4-8 \
  --parallel-processor ultra4x
```

Or set them once for your shell (or in `.env` alongside your API keys):

```bash
export KIMLIK_ANTHROPIC_MODEL="claude-opus-4-8"
export KIMLIK_OPENAI_PHASE1_MODEL="gpt-5.5-pro"
```

The models used are printed at startup and recorded in `kimlik_state.json`, so a finished run always states what produced it. Token budgets follow the *phase*, not the model name, so overriding a model never silently changes the output ceiling.

### Resuming an interrupted run

If the process is killed (Ctrl+C, network drop, timeout), just re-run the **exact same command**. The tool reads `kimlik_state.json` from the output directory and skips any provider that already completed.

The Parallel.ai task is especially long-running (up to 2 hours for `ultra8x`). Its `run_id` is saved to the state file immediately after submission, so a resume picks up polling the existing cloud task rather than resubmitting, and you are not billed twice.

```bash
# Same command; auto-detects state and resumes:
kimlik \
  --biopsy-site "right lung" \
  --tumor-diagnosis "metastatic osteosarcoma (primary: distal femur)" \
  --output-dir ./output_osteo_lung
```

### Starting fresh

```bash
kimlik \
  --biopsy-site "right lung" \
  --tumor-diagnosis "metastatic osteosarcoma (primary: distal femur)" \
  --output-dir ./output_osteo_lung \
  --force
```

`--force` ignores the existing state file and submits all providers again, at full cost. Use a different `--output-dir` to preserve the previous run's files.

## Troubleshooting

**`kimlik: command not found`**
Either you skipped `uv sync`, or you dropped the `uv run` prefix. From inside the kimlik folder, run `uv run kimlik --help`. If you installed with pip instead, activate the environment first (`source .venv/bin/activate`).

**`uv: command not found`, right after installing uv**
Close the terminal and open a new one. The installer edits your shell configuration, which only takes effect in a fresh session.

**`Cannot start: missing API key(s)`**
kimlik looks for a `.env` file **in the folder you run it from**, not in the folder where it was installed. The error prints the directory it checked. Either create `.env` there, or set the keys in your shell environment. Check also that you replaced the placeholder values, and that there are no spaces around the `=`.

**Nothing has printed for a long time. Is it stuck?**
Almost certainly not. Deep research runs for tens of minutes with no visible activity, so each long wait prints a heartbeat every 5 minutes (`Parallel.ai still researching: 15 min elapsed`). If you are seeing those, it is working. Leave it. If you do interrupt it, re-running the same command resumes rather than restarting.

**`ModuleNotFoundError: No module named 'parallel'`**
The package is installed as `parallel-web` but imported as `parallel`. Run `uv sync` (or `pip install .`).

**A provider `returned an empty report`**
The model spent its whole budget searching without ever writing the report. Nothing is saved, because an empty file would silently flow into the next phase. Re-run the same command: finished providers are skipped and only the failed one is retried.

**A provider returns `model not found`**
Your account probably lacks access to a default model. Override it without touching the source; see [Choosing models](#choosing-models):

```bash
kimlik -b "..." -t "..." --openai-phase1-model gpt-5.1 --anthropic-model claude-sonnet-5
```

Any tool-capable Claude model works for the Anthropic phases; the agentic loop does not depend on a specific one.

**Parallel.ai task times out**
The poll budget is 7200 s (`_POLL_TIMEOUT_SECONDS` in `parallel_provider.py`). The tool retries polling automatically across restarts, so just re-run the same command. Check the active `task_id` in `kimlik_state.json` if you want to monitor it on the Parallel.ai dashboard.

**Phase 2 fails but Phase 1 is complete**
Re-run the same command. Phase 1 outputs are cached; only Phase 2 providers with non-`completed` status will be retried.

**A report looks complete but cites references that are not listed**
It was truncated at the token ceiling. See [Output length and truncation](#output-length-and-truncation).

## Architecture notes

### State and resume

The file `kimlik_state.json` in the output directory tracks the status of every provider task:

```json
{
  "biopsy_site": "right lung",
  "tumor_diagnosis": "metastatic osteosarcoma (primary: distal femur)",
  "models": {
    "openai_phase1": "gpt-5.5-pro",
    "openai_phase2": "gpt-5.5",
    "anthropic": "claude-opus-5",
    "parallel_processor": "ultra8x"
  },
  "phase1": {
    "openai":    { "status": "completed", "output_file": "phase1_openai.md", ... },
    "parallel":  { "status": "running",   "task_id": "trun_abc123", ... },
    "anthropic": { "status": "pending",   ... }
  },
  "phase2": { ... }
}
```

Possible statuses: `pending` -> `running` -> `completed` / `failed`.

On resume, `completed` providers are skipped. `failed` providers are retried. For Parallel.ai, if `task_id` is present, polling resumes on the existing cloud task rather than creating a new one.

Changing models between resumes is allowed, which is useful for retrying one failed provider on a different model. The tool prints a notice when the current models differ from those recorded, and outputs already on disk keep whichever model produced them.

### Output length and truncation

These reports are long (dense marker tables followed by a full bibliography), so the output token ceiling matters more than it usually does. When a response is cut short it is cut short **at the end**, which is exactly where the references live: you get a document that looks complete but cites `[42]` with no reference list to resolve it.

Current ceilings: 100K tokens for OpenAI Phase 1, 64K for OpenAI Phase 2, and 64K for every Anthropic call. At the Anthropic ceiling the SDK requires streaming, so the tool loop consumes a stream and assembles the final message rather than issuing a plain request.

Both providers now report truncation rather than swallowing it: OpenAI on an `incomplete` response status, Anthropic on `stop_reason == "max_tokens"`. If you see that warning, raise the relevant constant and re-run the affected phase; completed phases are cached, so only the truncated one is redone.

A quick sanity check on any run: a complete report ends with its last reference, not mid-sentence or mid-table-row.

The other end of the same problem is a report that never gets written at all. A model can spend every tool round searching and return nothing, so any output shorter than 500 characters is rejected as a failure instead of being saved and passed to the next phase.

### Anthropic: PubMed and web search

The Anthropic provider runs an agentic tool loop with two tools enabled in Phase 1:

- **`web_search`** (`web_search_20250305`): Anthropic-hosted web search. Anthropic's infrastructure handles the fetch server-side.
- **`pubmed_search`**: Custom tool via the [NCBI E-utilities API](https://www.ncbi.nlm.nih.gov/books/NBK25499/) (free, no key required). Searches PubMed and returns abstracts for the model to cite.

Phase 2 consolidation runs without tools; the model only synthesises the three provided reports.

### Parallel.ai: synchronous SDK in async context

The `parallel-web` SDK is synchronous. It runs inside `asyncio.run_in_executor()` (a thread pool) so it does not block the event loop while OpenAI and Anthropic run concurrently.

## Development

```bash
uv sync --group dev

uv run pytest        # 93 tests, under a second
uv run ruff check .
```

The test suite mocks every provider SDK, so it needs no API keys and makes no network calls, so running it costs nothing. CI runs the same two commands on Python 3.11, 3.12, and 3.13, plus a build that installs the wheel and checks the CLI entry point.

Note that several tests are regression guards for bugs that were subtle in production: silent truncation at the provider token ceilings, per-phase token budgets, and rich swallowing bracketed text in log lines and `--help`. If one of those fails, read the test's docstring before changing it.

## Project structure

```
kimlik/
├── src/kimlik/
│   ├── __init__.py
│   ├── cli.py                # CLI entrypoint and async pipeline orchestration
│   ├── config.py             # model selection (CLI flag > env var > default)
│   ├── state.py              # JSON state read/write with atomic file ops
│   ├── prompts.py            # Phase 1, consolidation, and final-merge prompt templates
│   └── providers/
│       ├── openai_provider.py        # AsyncOpenAI (Responses API)
│       ├── parallel_provider.py      # parallel-web SDK (submit + poll with retry)
│       └── anthropic_provider.py     # AsyncAnthropic with agentic tool loop
├── tests/                    # offline suite; every provider SDK is mocked
├── results/
│   └── example-osteosarcoma-lung-met/  # committed demo run (see the example above)
├── .github/workflows/ci.yml  # lint, test matrix, package build
├── pyproject.toml            # package metadata, deps, ruff + pytest config
├── requirements.txt          # pip fallback
├── .python-version           # pins Python 3.11 for uv
├── .env.example              # copy to .env and fill in keys
└── README.md
```

## Related

- **[kopya](https://github.com/ValiusSciences/kopya)**: expression-only single-cell copy-number-variation caller.

*kopya reads the genome's copies; kimlik reads its identities.*

## License

MIT. See [LICENSE](LICENSE).
