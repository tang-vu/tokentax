"""Tests for the two-corpus comparison.

This logic decides which conclusions count as replicated, so it is worth
holding to the same standard as the measurement itself.
"""

import pytest

from tokentax import cross_check
from tokentax.results import BenchmarkRun, Measurement


def measurement(tokenizer, language, tax, pairs=500, lossy=False, legacy=False):
    return Measurement(
        tokenizer=tokenizer,
        tokenizer_label=tokenizer.upper(),
        language=language[:2],
        language_name=language,
        pairs=pairs,
        english_tokens=1000,
        target_tokens=int(1000 * tax),
        tax=tax,
        median_ratio=tax,
        p90_ratio=tax,
        target_tokens_per_char=0.3,
        lossy=lossy,
        legacy=legacy,
    )


def run(measurements, source="opus-100", name="corpus"):
    return BenchmarkRun(
        measurements=list(measurements), corpus_source=source, corpus_name=name
    )


def test_identical_runs_agree_completely():
    rows = [measurement("aya", "Tamil", 1.3), measurement("mistral", "Tamil", 5.0)]
    result = cross_check.compare(run(rows), run(rows))
    assert len(result) == 1
    assert result[0].median_drift == 0.0
    assert result[0].cheapest_agrees
    assert result[0].dearest_agrees


def test_absolute_shift_without_rank_change_is_reported_as_drift_only():
    # Both tokenizers get 20% dearer; the advice is unchanged.
    a = run([measurement("aya", "Tamil", 1.0), measurement("mistral", "Tamil", 5.0)])
    b = run([measurement("aya", "Tamil", 1.2), measurement("mistral", "Tamil", 6.0)])
    row = cross_check.compare(a, b)[0]
    assert row.median_drift == pytest.approx(0.2)
    assert row.cheapest_agrees
    assert row.dearest_agrees


def test_flipped_ranking_is_surfaced():
    a = run([measurement("aya", "Tamil", 1.0), measurement("mistral", "Tamil", 5.0)])
    b = run([measurement("aya", "Tamil", 5.0), measurement("mistral", "Tamil", 1.0)])
    row = cross_check.compare(a, b)[0]
    assert not row.cheapest_agrees
    assert row.cheapest_a == "aya" and row.cheapest_b == "mistral"


def test_only_tokenizers_present_in_both_runs_are_compared():
    a = run(
        [
            measurement("aya", "Tamil", 1.0),
            measurement("mistral", "Tamil", 5.0),
            measurement("only-in-a", "Tamil", 0.1),
        ]
    )
    b = run([measurement("aya", "Tamil", 1.0), measurement("mistral", "Tamil", 5.0)])
    row = cross_check.compare(a, b)[0]
    # The unmatched tokenizer is cheapest in a, but comparing it to nothing
    # would manufacture a disagreement.
    assert row.cheapest_a == "aya"
    assert row.cheapest_agrees


def test_languages_missing_from_one_run_are_skipped():
    a = run([measurement("aya", "Tamil", 1.0), measurement("aya", "Khmer", 2.0)])
    b = run([measurement("aya", "Tamil", 1.0)])
    result = cross_check.compare(a, b)
    assert [r.language for r in result] == ["Tamil"]


def test_lossy_and_legacy_cells_are_excluded():
    a = run(
        [
            measurement("aya", "Tamil", 1.0),
            measurement("broken", "Tamil", 0.1, lossy=True),
            measurement("gpt2", "Tamil", 9.0, legacy=True),
        ]
    )
    b = run(
        [
            measurement("aya", "Tamil", 1.0),
            measurement("broken", "Tamil", 0.1, lossy=True),
            measurement("gpt2", "Tamil", 9.0, legacy=True),
        ]
    )
    row = cross_check.compare(a, b)[0]
    assert row.cheapest_a == "aya"
    assert row.dearest_a == "aya"


def test_rows_are_ordered_worst_agreement_first():
    a = run([measurement("aya", "Tamil", 1.0), measurement("aya", "Khmer", 1.0)])
    b = run([measurement("aya", "Tamil", 1.1), measurement("aya", "Khmer", 2.0)])
    result = cross_check.compare(a, b)
    assert [r.language for r in result] == ["Khmer", "Tamil"]


def test_markdown_reports_counts_and_flags_large_drift():
    a = run([measurement("aya", "Tamil", 1.0), measurement("mistral", "Tamil", 5.0)])
    b = run([measurement("aya", "Tamil", 2.0), measurement("mistral", "Tamil", 10.0)])
    text = cross_check.to_markdown(a, b, cross_check.compare(a, b))
    assert "Cheapest tokenizer agrees for **1 of 1**" in text
    assert "⚠" in text  # 100% drift is past the notable threshold


def test_markdown_handles_runs_with_nothing_in_common():
    a = run([measurement("aya", "Tamil", 1.0)])
    b = run([measurement("aya", "Khmer", 1.0)])
    assert "share no languages" in cross_check.to_markdown(a, b, [])
