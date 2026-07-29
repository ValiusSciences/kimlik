# Phase 1: each provider independently researches and generates a report.
# The "Attached are three reports" line from the user's original prompt is intentionally
# omitted here because no reports exist yet — each provider generates its own from scratch.
PHASE1_PROMPT = (
    "I have single-cell sequencing data from a patient's biopsy ({biopsy_site}). "
    "This patient was originally diagnosed with a {tumor_diagnosis}. "
    "I would like to compile a list of genes that can be used as gene signatures "
    "to identify different types of cells we are seeing in the single-cell sequencing data. "
    "These cell types should ideally be clinically known and characterized ones. "
    "Please create a comprehensive report in markdown format. "
    "Search the latest literature thoroughly and include all relevant references to "
    "peer-reviewed publications. Do not drop the references."
)

# Phase 2: all three Phase 1 reports are prepended as context before this prompt.
CONSOLIDATION_PROMPT = (
    "I have single-cell sequencing data from a patient's biopsy ({biopsy_site}). "
    "This patient was originally diagnosed with a {tumor_diagnosis}. "
    "I would like to compile a list of genes that can be used as gene signatures "
    "to identify different types of cells we are seeing in the single-cell sequencing data. "
    "These cell types should ideally be clinically known and characterized ones. "
    "Attached are three comprehensive reports on different cell types and their signatures "
    "with pointers to reliable publications. "
    "Help me create a consensus final report in markdown format. Don't drop the references."
)

# Phase 3: the two Phase 2 consensus reports are prepended before this prompt.
FINAL_PROMPT = (
    "I have single-cell sequencing data from a patient's biopsy ({biopsy_site}). "
    "This patient was originally diagnosed with a {tumor_diagnosis}. "
    "Attached are two independent consensus reports on gene signatures for "
    "labeling cell types from the scRNA-seq data. "
    "Please merge them into one definitive final guide: consolidate overlapping sections, "
    "resolve any contradictions by deferring to the best-supported evidence, and ensure "
    "every reference is preserved. Output a single, well-structured markdown document."
)

def format_phase1(biopsy_site: str, tumor_diagnosis: str) -> str:
    return PHASE1_PROMPT.format(biopsy_site=biopsy_site, tumor_diagnosis=tumor_diagnosis)


def format_final(
    biopsy_site: str,
    tumor_diagnosis: str,
    openai_consensus: str,
    anthropic_consensus: str,
    labels: dict[str, str],
) -> str:
    reports = (
        f"## Consensus Report 1 — {labels['openai']}\n\n{openai_consensus}"
        "\n\n---\n\n"
        f"## Consensus Report 2 — {labels['anthropic']}\n\n{anthropic_consensus}"
    )
    prompt = FINAL_PROMPT.format(biopsy_site=biopsy_site, tumor_diagnosis=tumor_diagnosis)
    return f"{reports}\n\n---\n\n{prompt}"


def format_consolidation(
    biopsy_site: str,
    tumor_diagnosis: str,
    reports: dict[str, str],
    labels: dict[str, str],
) -> str:
    parts = []
    for key, content in reports.items():
        label = labels.get(key, key)
        parts.append(f"## Report from {label}\n\n{content}")

    all_reports = "\n\n---\n\n".join(parts)
    prompt = CONSOLIDATION_PROMPT.format(
        biopsy_site=biopsy_site, tumor_diagnosis=tumor_diagnosis
    )
    return f"{all_reports}\n\n---\n\n{prompt}"
