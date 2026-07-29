# kimlik

**Tissue- and diagnosis-specific gene signatures for labeling cell types in single-cell RNA-seq data.**

`kimlik` (Turkish for *identity*) is a command-line tool that generates a consensus gene-signature report for annotating scRNA-seq data, tailored to a specific biopsy site and tumor diagnosis. Instead of reaching for a generic marker panel, you get a literature-backed reference for the tissue and disease context you are actually working in.

It queries three LLM providers in parallel, has two of them independently consolidate the results, then merges those into a single definitive guide, with citations to peer-reviewed literature at every step.

---

## What you get

One Markdown guide you can read or hand to a collaborator. Here is a fragment of the [committed example run](results/example-osteosarcoma-lung-met/phase3_final.md), a lung biopsy of metastatic osteosarcoma:

| Cell type | Core markers | Notes | Refs |
|---|---|---|---|
| **Lung epithelium** | `EPCAM, KRT8, KRT18, KRT19, CDH1` | Surfactant RNA is often ambient; require coherent co-expression | [52-57] |
| **Mesothelium (pleura)** | `MSLN, UPK3B, WT1, CALB2, ITLN1` | Common in pleural-based biopsies; frequently misannotated | [52, 53, 65] |
| **Skeletal myocyte / myoblast** | `MYL1, MYLPF, TNNT1, ACTA1, MYOD1` | Discrete cluster in limb osteosarcoma; **should be absent in lung** | [1] |
| **Cycling (any lineage)** | `MKI67, TOP2A, CCNB1, CENPF, PCNA` | Annotate as "cycling (parent lineage)", never as its own type | [118] |

That guide is 82 KB with 145 references. **Read it before you run anything.** It costs nothing and shows exactly what the tool produces.

---

## Why site-specific panels matter

For a primary tumor, a stock tissue panel usually gets you most of the way. The problem appears once disease spreads, because **a metastatic biopsy contains cells that do not belong to the tissue it was taken from.**

Take osteosarcoma that has metastasized to lung, the example shipped in this repo. That biopsy holds three populations at once:

- **Lung parenchyma and stroma** native to the biopsy site: AT1/AT2 pneumocytes, club and ciliated cells, alveolar macrophages.
- **Osteoblastic tumor cells** carrying their bone lineage program (`RUNX2`, `SP7`, `COL1A1`, `ALPL`, `IBSP`), sitting in tissue where no bone markers belong.
- **A tumor microenvironment** shaped by both.

A generic lung panel silently mislabels the tumor compartment; a generic bone panel misses the microenvironment. `kimlik` is built for exactly this case: you give it both the site *and* the diagnosis, and the report covers the resident tissue, the metastatic tumor lineage, and the immune and stromal compartments together.

---

## Before you start

kimlik is neither free nor fast. Know this before your first run:

- It calls **three paid APIs**: OpenAI, Anthropic, and Parallel.ai. You need an account with billing enabled at all three. There is no single-provider mode; the cross-checking between them is the point.
- A run takes **30 minutes to 2 hours**, most of it waiting on deep research.
- You need **Python 3.11 or newer**.

**What it costs.** The example run in this repo produced 316 KB of reports, roughly 80,000 output tokens across six model calls, plus about 90,000 tokens of input for the consolidation and merge steps. The Parallel.ai processor and the OpenAI reasoning model dominate the bill.

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

---

## Quick start

```bash
# 1. Install
git clone <this-repo> && cd kimlik
uv sync

# 2. Add your three API keys
cp .env.example .env     # then open .env and paste your keys in

# 3. Run
uv run kimlik \
  -b "right lung" \
  -t "metastatic osteosarcoma (primary: distal femur)" \
  -o ./my_run
```

When it finishes, read `my_run/phase3_final.md`. If the run is interrupted at any point, re-run the exact same command and it picks up where it left off without repaying for finished work.

The sections below cover installation alternatives, keys, and every option in detail.

---

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

All outputs are saved to a folder you specify. A state file (`kimlik_state.json`) is written alongside the outputs so the tool can **resume** from exactly where it left off if interrupted.

---

## Installation

### With uv (recommended)

[uv](https://docs.astral.sh/uv/) manages the Python version, virtual environment, and package installation automatically.

```bash
# Install uv (once, system-wide)
curl -LsSf https://astral.sh/uv/install.sh | sh   # macOS/Linux
# winget install astral-sh.uv                      # Windows

git clone <this-repo>
cd kimlik

uv sync          # creates .venv, installs deps, and installs the kimlik command
```

The `kimlik` command is now available:

```bash
uv run kimlik --help
```

### With pip

```bash
git clone <this-repo>
cd kimlik

python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# .venv\Scripts\activate         # Windows

pip install .
kimlik --help
```

---

## API Keys

The tool reads credentials from environment variables. There are three ways to provide them, in order of preference:

### Option 1: `.env` file (recommended for local use)

```bash
cp .env.example .env
```

Edit `.env`:

```dotenv
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PARALLEL_API_KEY=...
```

The tool loads this file automatically on startup. The `.env` file is gitignored and should never be committed.

### Option 2: Shell environment variables

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export PARALLEL_API_KEY="..."
```

### Option 3: Inline for a single run

```bash
OPENAI_API_KEY="sk-..." ANTHROPIC_API_KEY="sk-ant-..." PARALLEL_API_KEY="..." \
  kimlik --biopsy-site "..." --tumor-diagnosis "..."
```

### Where to get each key

| Provider | Key name | Where to get it |
|---|---|---|
| OpenAI | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| Anthropic | `ANTHROPIC_API_KEY` | https://console.anthropic.com/settings/keys |
| Parallel.ai | `PARALLEL_API_KEY` | https://app.parallel.ai > Settings > API Keys |

---

## Usage

### Basic run

```bash
kimlik \
  --biopsy-site "right lung" \
  --tumor-diagnosis "metastatic osteosarcoma (primary: distal femur)" \
  --output-dir ./output_osteo_lung
```

### All options

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

The Parallel.ai task is especially long-running (up to 2 hours for `ultra8x`). Its `run_id` is saved to the state file immediately after submission, so a resume picks up polling the existing cloud task rather than resubmitting.

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

`--force` ignores the existing state file and submits all providers again. Use a different `--output-dir` to preserve the previous run's files.

---

## Output files

After a successful run, the output directory contains:

```
output_osteo_lung/
├── kimlik_state.json             # run state (do not delete while running)
├── phase1_openai.md              # OpenAI gpt-5.5-pro independent report
├── phase1_parallel.md            # Parallel.ai ultra8x deep-research report
├── phase1_anthropic.md           # Anthropic claude-opus-5 report (with PubMed + web search)
├── phase2_openai_consensus.md    # OpenAI gpt-5.5 consensus of all 3 reports
├── phase2_anthropic_consensus.md # Anthropic claude-opus-5 consensus of all 3 reports
└── phase3_final.md               # single definitive guide (merger of both Phase 2 reports)
```

All files are plain Markdown.

---

## Example output

A complete run is committed under [`results/example-osteosarcoma-lung-met/`](results/example-osteosarcoma-lung-met/) so you can read real output before spending an API budget. It uses the metastatic case described above, a synthetic textbook presentation rather than a real patient:

```bash
kimlik \
  -b "right lung" \
  -t "metastatic osteosarcoma (primary: distal femur)" \
  -o results/example-osteosarcoma-lung-met
```

Start with [`phase3_final.md`](results/example-osteosarcoma-lung-met/phase3_final.md): the single merged guide, ~82 KB with 145 references and no dangling citations. The Phase 1 and Phase 2 files are kept alongside it so you can see how three independent literature searches converged, and where they disagreed.

| File | Size | Produced by |
|---|---|---|
| `phase1_openai.md` | 35 KB | OpenAI `gpt-5.5-pro` |
| `phase1_parallel.md` | 32 KB | Parallel.ai `ultra8x` (44 min) |
| `phase1_anthropic.md` | 49 KB | Anthropic `claude-opus-5` + PubMed/web search |
| `phase2_openai_consensus.md` | 42 KB | OpenAI `gpt-5.5` |
| `phase2_anthropic_consensus.md` | 76 KB | Anthropic `claude-opus-5` |
| `phase3_final.md` | 82 KB | Anthropic `claude-opus-5` |

The structure of the final guide is the argument for the tool: alongside the malignant osteosarcoma compartment (`RUNX2`, `SP7`, `COL1A1`, `ALPL`, `IBSP`) and the resident lung epithelium (`SFTPC`, `AGER`, `SCGB1A1`, `FOXJ1`), it devotes a whole section to *differential diagnosis in a lung biopsy*, a section that exists only because the site and the diagnosis disagree.

This is the only run committed to the repository; everything else under `results/` is gitignored by default so real cases cannot be pushed by accident.

---

## Data and privacy

**Do not pass protected health information to this tool.**

`kimlik` takes only two inputs, a biopsy site and a tumor diagnosis, and both are transmitted to third-party LLM APIs (OpenAI, Anthropic, Parallel.ai) as prompt text. Keep them at the level of clinical description (`"right lung"`, `"metastatic osteosarcoma"`). Never include names, medical record numbers, dates of birth, accession numbers, or any other identifier.

The tool never reads your expression matrices, count files, or any patient-level data. Its outputs are literature-derived marker panels containing no patient information, but if you organize output directories by case, treat those directories as you would any other study artifact and keep them out of version control.

---

## Runtime expectations

| Provider | Typical duration | Notes |
|---|---|---|
| OpenAI gpt-5.5-pro | 2–10 min | Reasoning model; duration varies with output length |
| Parallel.ai ultra8x | 5 min – 2 hr | Deep multi-source research; most thorough |
| Anthropic claude-opus-5 | 3–15 min | Runs an agentic tool loop with PubMed + web search |
| Phase 2 consolidation | 2–8 min | Runs after all Phase 1 outputs are ready |
| Phase 3 final merge | 2–5 min | Runs after both Phase 2 reports are ready |

Phase 1 providers run **concurrently**, so total wall time is determined by the slowest one (usually Parallel.ai).

---

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

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'parallel'`**
The package is installed as `parallel-web` but imported as `parallel`. Run `uv sync` (or `pip install .`).

**Nothing has printed for a long time. Is it stuck?**
Almost certainly not. Deep research runs for tens of minutes with no visible activity, so each long wait prints a heartbeat every 5 minutes (`Parallel.ai still researching: 15 min elapsed`). If you are seeing those, it is working. Leave it. If you do interrupt it, re-running the same command resumes rather than restarting.

**`Cannot start: missing API key(s)`**
kimlik looks for a `.env` file **in the folder you run it from**, not in the folder where it was installed. The error prints the directory it checked. Either create `.env` there, or set the keys in your shell environment.

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

---

## Development

```bash
uv sync --group dev

uv run pytest        # 61 tests, ~1s
uv run ruff check .
```

The test suite mocks every provider SDK, so it needs no API keys and makes no network calls, so running it costs nothing. CI runs the same two commands on Python 3.11, 3.12, and 3.13, plus a build that installs the wheel and checks the CLI entry point.

Note that several tests are regression guards for bugs that were subtle in production: silent truncation at the provider token ceilings, per-phase token budgets, and rich swallowing bracketed text in log lines and `--help`. If one of those fails, read the test's docstring before changing it.

---

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
│   └── example-osteosarcoma-lung-met/  # committed demo run (see Example output)
├── .github/workflows/ci.yml  # lint, test matrix, package build
├── pyproject.toml            # package metadata, deps, ruff + pytest config
├── requirements.txt          # pip fallback
├── .python-version           # pins Python 3.11 for uv
├── .env.example              # copy to .env and fill in keys
└── README.md
```

---

## Related

- **[kopya](https://github.com/ValiusSciences/kopya)**: expression-only single-cell copy-number-variation caller.

*kopya reads the genome's copies; kimlik reads its identities.*

---

## License

MIT. See [LICENSE](LICENSE).
