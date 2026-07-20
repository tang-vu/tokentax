"""Compare two benchmark runs measured on different corpora.

A single dataset can carry a quirk that biases every figure derived from it —
OPUS-100's Khmer portion, for instance, arrived 39% full of HTML entities. The
only way to catch that class of error is to measure somewhere else and see
which conclusions survive.

This module answers two questions:

* do the *numbers* agree — is the tax for a language roughly the same on both?
* do the *rankings* agree — would a reader pick the same tokenizer either way?

The second matters more. Absolute tax shifts with domain and register, so some
drift is expected and harmless. A flipped ranking means the advice changes.
"""

from __future__ import annotations

import statistics
from dataclasses import dataclass

from .results import BenchmarkRun

# Two runs measured on different text will never agree exactly. Beyond this
# relative gap the disagreement is worth a reader's attention rather than being
# waved off as domain drift.
NOTABLE_DRIFT = 0.25


@dataclass(frozen=True)
class LanguageAgreement:
    """How well the two corpora agree about one language."""

    language: str
    pairs_a: int
    pairs_b: int
    median_drift: float  # median |b-a|/a across shared tokenizers
    cheapest_a: str
    cheapest_b: str
    dearest_a: str
    dearest_b: str

    @property
    def cheapest_agrees(self) -> bool:
        return self.cheapest_a == self.cheapest_b

    @property
    def dearest_agrees(self) -> bool:
        return self.dearest_a == self.dearest_b


def compare(a: BenchmarkRun, b: BenchmarkRun) -> list[LanguageAgreement]:
    """Compare runs language by language, worst agreement first."""
    from .ranking import deployable

    index_a = {(m.language_name, m.tokenizer): m for m in a.measurements}
    index_b = {(m.language_name, m.tokenizer): m for m in b.measurements}
    shared_languages = sorted(
        {lang for lang, _ in index_a} & {lang for lang, _ in index_b}
    )

    rows: list[LanguageAgreement] = []
    for language in shared_languages:
        rows_a = deployable(
            [m for m in a.measurements if m.language_name == language]
        )
        rows_b = deployable(
            [m for m in b.measurements if m.language_name == language]
        )
        shared = {m.tokenizer for m in rows_a} & {m.tokenizer for m in rows_b}
        if not shared:
            continue

        drifts = [
            abs(index_b[(language, key)].tax - index_a[(language, key)].tax)
            / index_a[(language, key)].tax
            for key in shared
            if index_a[(language, key)].tax
        ]
        best_a = min((m for m in rows_a if m.tokenizer in shared), key=_tax)
        best_b = min((m for m in rows_b if m.tokenizer in shared), key=_tax)
        worst_a = max((m for m in rows_a if m.tokenizer in shared), key=_tax)
        worst_b = max((m for m in rows_b if m.tokenizer in shared), key=_tax)

        rows.append(
            LanguageAgreement(
                language=language,
                pairs_a=rows_a[0].pairs,
                pairs_b=rows_b[0].pairs,
                median_drift=statistics.median(drifts) if drifts else 0.0,
                cheapest_a=best_a.tokenizer,
                cheapest_b=best_b.tokenizer,
                dearest_a=worst_a.tokenizer,
                dearest_b=worst_b.tokenizer,
            )
        )

    rows.sort(key=lambda r: -r.median_drift)
    return rows


def _tax(measurement) -> float:
    return measurement.tax


def to_markdown(a: BenchmarkRun, b: BenchmarkRun, rows: list[LanguageAgreement]) -> str:
    if not rows:
        return "# Cross-check\n\nThe two runs share no languages.\n"

    agree_cheapest = sum(1 for r in rows if r.cheapest_agrees)
    agree_dearest = sum(1 for r in rows if r.dearest_agrees)
    drifts = [r.median_drift for r in rows]

    lines = [
        "# Cross-check: does this replicate on a second corpus?",
        "",
        f"`{a.corpus_name}` ({a.corpus_source}) versus `{b.corpus_name}` "
        f"({b.corpus_source}), over the {len(rows)} languages both cover.",
        "",
        "The first corpus is crawled; the second is professionally translated. "
        "They share no text, so agreement is evidence the figures describe "
        "tokenizers rather than one dataset's habits.",
        "",
        "## Summary",
        "",
        f"- Cheapest tokenizer agrees for **{agree_cheapest} of {len(rows)}** languages.",
        f"- Most expensive agrees for **{agree_dearest} of {len(rows)}**.",
        f"- Median tax drift across all languages: **{statistics.median(drifts):.0%}**.",
        "",
        "Absolute tax is expected to move between corpora — register and domain "
        "differ. A changed *ranking* is the finding that matters, because that "
        "is what changes the advice.",
        "",
        "## By language",
        "",
        "| Language | Pairs (crawled / human) | Tax drift | Cheapest agrees | Dearest agrees |",
        "|---|---|---:|---|---|",
    ]
    for row in rows:
        cheap = "yes" if row.cheapest_agrees else f"**{row.cheapest_a} → {row.cheapest_b}**"
        dear = "yes" if row.dearest_agrees else f"**{row.dearest_a} → {row.dearest_b}**"
        flag = " ⚠" if row.median_drift > NOTABLE_DRIFT else ""
        lines.append(
            f"| {row.language} | {row.pairs_a} / {row.pairs_b} "
            f"| {row.median_drift:.0%}{flag} | {cheap} | {dear} |"
        )
    return "\n".join(lines) + "\n"
