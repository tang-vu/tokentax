"""Markdown table renderers.

Each function returns a list of lines including its own section heading, so
:mod:`report` only decides which sections appear and in what order.
"""

from __future__ import annotations

from .benchmark import BenchmarkRun
from .ranking import deployable


def matrix(
    run: BenchmarkRun,
    tokenizers: list[tuple[str, str]],
    languages: list[tuple[str, str]],
) -> list[str]:
    """Full language x tokenizer grid of tax values."""
    lookup = {(m.tokenizer, m.language): m for m in run.measurements}
    header = "| Language | " + " | ".join(label for _, label in tokenizers) + " |"
    divider = "|---|" + "|".join(["---:"] * len(tokenizers)) + "|"
    rows = [header, divider]
    for code, name in languages:
        cells = []
        for key, _ in tokenizers:
            measurement = lookup.get((key, code))
            if measurement is None:
                cells.append("—")
            elif measurement.lossy:
                cells.append(f"{measurement.tax:.2f}x ⚠")
            else:
                cells.append(f"{measurement.tax:.2f}x")
        rows.append(f"| {name} | " + " | ".join(cells) + " |")
    return [
        "## Token tax by tokenizer",
        "",
        "`—` the tokenizer does not target that language. "
        "`⚠` the tokenizer emitted unknown tokens, so its count describes "
        "degraded text and is excluded from the rankings below. GPT-2 is "
        "included as a 2019 reference point, not as a live option.",
        "",
        *rows,
    ]


def spread(run: BenchmarkRun, languages: list[tuple[str, str]]) -> list[str]:
    """Cheapest vs most expensive tokenizer per language.

    This is the actionable table: the spread is what a team saves purely by
    switching tokenizer families, before any quality consideration.
    """
    rows = [
        "| Language | Cheapest | Tax | Most expensive | Tax | Overpay |",
        "|---|---|---:|---|---:|---:|",
    ]
    for code, name in languages:
        measurements = deployable(run.for_language(code))
        if not measurements:
            continue
        best = min(measurements, key=lambda m: m.tax)
        worst = max(measurements, key=lambda m: m.tax)
        overpay = worst.tax / best.tax if best.tax else float("nan")
        rows.append(
            f"| {name} | {best.tokenizer_label} | {best.tax:.2f}x "
            f"| {worst.tokenizer_label} | {worst.tax:.2f}x | **{overpay:.1f}x** |"
        )
    return [
        "## Cheapest vs most expensive tokenizer",
        "",
        "`Overpay` is how much more the worst tokenizer costs than the best one "
        "for the same text.",
        "",
        *rows,
    ]


def context_window(
    run: BenchmarkRun, languages: list[tuple[str, str]], window: int = 128_000
) -> list[str]:
    """Token tax also shrinks the usable context window, not just the bill."""
    rows = ["| Language | Best case | Worst case |", "|---|---:|---:|"]
    for code, name in languages:
        measurements = deployable(run.for_language(code))
        if not measurements:
            continue
        best = min(m.tax for m in measurements)
        worst = max(m.tax for m in measurements)
        rows.append(
            f"| {name} | {int(window / best):,} tokens "
            f"| {int(window / worst):,} tokens |"
        )
    return [
        "## Effective context window",
        "",
        f"English content that fits in a nominal {window:,}-token window, "
        "expressed in tokens of that content's English original.",
        "",
        *rows,
    ]


def split_note(run: BenchmarkRun) -> list[str]:
    """Name the languages whose pairs came from a non-held-out split."""
    fallbacks = sorted(
        {
            (m.language_name, m.split)
            for m in run.measurements
            if m.split != run.corpus_split
        }
    )
    if not fallbacks:
        return []
    listed = ", ".join(f"{name} (`{split}`)" for name, split in fallbacks)
    return [
        "",
        f"> These languages have no `{run.corpus_split}` split in OPUS-100 and "
        f"were measured on another split: {listed}. Their text is not held out "
        "and, being lower-resource pairs, is likely noisier — treat those rows "
        "as indicative rather than precise.",
    ]


def methodology() -> list[str]:
    return [
        "## Methodology",
        "",
        "- Every number compares **aligned translations of the same sentence**, "
        "so differences reflect tokenizer efficiency rather than differing content.",
        "- Tax is aggregate: total target tokens / total English tokens across all "
        "pairs. Per-sentence median and p90 are in the JSON output.",
        "- Special tokens and chat templates are excluded; only content is counted.",
        "- OPUS-100 is crawled data, so pairs are filtered for length, alignment "
        "plausibility, duplicates, and untranslated rows before counting.",
        "- Cells where more than 1% of tokens are unknown are marked lossy and "
        "excluded from rankings: a tokenizer that drops characters can post a "
        "low token count while destroying the text.",
        "- Monolingual tokenizers are only measured against the language they "
        "target.",
        "- Historical tokenizers appear in the matrix but not in the rankings: "
        "GPT-2 is the worst option for every language, which is true and "
        "useless for choosing between tokenizers shipping today.",
        "",
        "Full limitations: [`docs/methodology-and-limitations.md`]"
        "(docs/methodology-and-limitations.md).",
    ]
