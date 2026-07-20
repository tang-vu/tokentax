"""Rendering of benchmark runs into Markdown and JSON.

The Markdown report leads with the matrix and then translates ratios into the
two consequences developers actually feel: a larger bill and a smaller usable
context window. Table bodies live in :mod:`report_tables`; selection and
ordering rules live in :mod:`ranking`.
"""

from __future__ import annotations

import json
from pathlib import Path

from . import report_tables
from .results import BenchmarkRun, Measurement
from .ranking import deployable, ordered_languages, ordered_tokenizers


def to_json(run: BenchmarkRun, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(run.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8"
    )


def to_markdown(run: BenchmarkRun) -> str:
    """Render a full report. English is the 1.00x baseline by construction."""
    if not run.measurements:
        return "# Token Tax\n\nNo measurements were produced.\n"

    tokenizers = ordered_tokenizers(run)
    languages = ordered_languages(run)

    lines = [
        "# Token Tax",
        "",
        "How many tokens a language costs relative to the **same sentence in "
        "English**. `1.00x` means parity with English; `2.00x` means every "
        "request costs twice as many tokens for identical content.",
        "",
        f"Corpus `{run.corpus_name}` (split `{run.corpus_split}`), "
        f"up to {run.samples_requested} aligned sentence pairs per language. "
        f"Generated {run.generated_at}.",
        "",
    ]

    lines.extend(report_tables.matrix(run, tokenizers, languages))
    lines.extend(report_tables.split_note(run))
    lines.append("")
    lines.extend(report_tables.spread(run, languages))
    lines.append("")
    lines.extend(report_tables.context_window(run, languages))

    if run.skipped:
        lines.extend(["", "## Skipped", ""])
        lines.extend(
            f"- `{key}`: {reason}" for key, reason in sorted(run.skipped.items())
        )

    lines.append("")
    lines.extend(report_tables.methodology())
    return "\n".join(lines) + "\n"


def summarize(run: BenchmarkRun) -> str:
    """One-screen terminal summary."""
    if not run.measurements:
        return "no measurements"
    lines = []
    for code, name in ordered_languages(run):
        measurements: list[Measurement] = deployable(run.for_language(code))
        best = min(measurements, key=lambda m: m.tax)
        worst = max(measurements, key=lambda m: m.tax)
        lines.append(
            f"{name:<12} best {best.tax:>5.2f}x ({best.tokenizer})"
            f"   worst {worst.tax:>5.2f}x ({worst.tokenizer})"
        )
    return "\n".join(lines)
