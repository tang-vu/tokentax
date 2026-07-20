"""Tests for report rendering, especially the handling of lossy cells."""

from tokentax import report
from tokentax.results import BenchmarkRun, Measurement


def make_measurement(
    tokenizer: str,
    language: str,
    tax: float,
    lossy: bool = False,
    legacy: bool = False,
    split: str = "test",
):
    return Measurement(
        tokenizer=tokenizer,
        tokenizer_label=tokenizer.upper(),
        language=language,
        language_name={"vi": "Vietnamese", "th": "Thai"}[language],
        pairs=100,
        english_tokens=1000,
        target_tokens=int(1000 * tax),
        tax=tax,
        median_ratio=tax,
        p90_ratio=tax,
        target_tokens_per_char=0.3,
        unknown_rate=0.5 if lossy else 0.0,
        lossy=lossy,
        legacy=legacy,
        split=split,
    )


def build_run(measurements) -> BenchmarkRun:
    return BenchmarkRun(
        measurements=list(measurements),
        samples_requested=100,
        generated_at="2026-07-20T00:00:00+00:00",
    )


def test_empty_run_renders_without_crashing():
    assert "No measurements" in report.to_markdown(build_run([]))


def test_lossy_cell_is_marked_in_matrix():
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("phobert", "vi", 0.72, lossy=True),
        ]
    )
    markdown = report.to_markdown(run)
    assert "0.72x ⚠" in markdown


def test_lossy_cell_is_excluded_from_best_and_worst():
    # The lossy tokenizer has the lowest tax, but rewarding it would mean
    # rewarding a tokenizer that destroyed the text.
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("mistral", "vi", 2.10),
            make_measurement("broken", "vi", 0.40, lossy=True),
        ]
    )
    markdown = report.to_markdown(run)
    assert "1.19x" in markdown
    # Overpay must be 2.10/1.19, not 2.10/0.40.
    assert "**1.8x**" in markdown


def test_legacy_tokenizer_shown_in_matrix_but_not_ranked():
    # GPT-2 is the worst option for every language; ranking it would be true
    # and useless for choosing among tokenizers shipping today.
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("mistral", "vi", 2.10),
            make_measurement("gpt2", "vi", 3.29, legacy=True),
        ]
    )
    markdown = report.to_markdown(run)
    assert "3.29x" in markdown  # still visible in the matrix
    # Overpay must be 2.10/1.19, not 3.29/1.19.
    assert "**1.8x**" in markdown
    assert "**2.8x**" not in markdown


def test_legacy_only_language_still_ranked():
    # If nothing modern was measured, fall back rather than dropping the row.
    run = build_run([make_measurement("gpt2", "vi", 3.29, legacy=True)])
    assert "GPT2" in report.to_markdown(run)


def test_summary_prefers_reliable_measurements():
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("broken", "vi", 0.40, lossy=True),
        ]
    )
    assert "o200k" in report.summarize(run)
    assert "broken" not in report.summarize(run)


def test_languages_ordered_by_mean_tax_descending():
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("o200k", "th", 2.50),
        ]
    )
    markdown = report.to_markdown(run)
    assert markdown.index("| Thai |") < markdown.index("| Vietnamese |")


def test_fallback_split_is_disclosed():
    # A train-split row is not held out; the report must say so rather than
    # presenting it as equivalent to the others.
    run = build_run(
        [
            make_measurement("o200k", "vi", 1.19),
            make_measurement("o200k", "th", 2.50, split="train"),
        ]
    )
    markdown = report.to_markdown(run)
    assert "Thai (`train`)" in markdown
    assert "not held out" in markdown


def test_no_split_note_when_every_row_used_the_requested_split():
    run = build_run([make_measurement("o200k", "vi", 1.19)])
    assert "not held out" not in report.to_markdown(run)


def test_skipped_entries_are_reported():
    run = build_run([make_measurement("o200k", "vi", 1.19)])
    run.skipped["llama3"] = "gated repo"
    markdown = report.to_markdown(run)
    assert "## Skipped" in markdown
    assert "gated repo" in markdown


def test_json_roundtrip_preserves_measurements(tmp_path):
    import json

    run = build_run([make_measurement("o200k", "vi", 1.19)])
    path = tmp_path / "out" / "token-tax.json"
    report.to_json(run, path)
    loaded = json.loads(path.read_text(encoding="utf-8"))
    assert loaded["measurements"][0]["tokenizer"] == "o200k"
    assert loaded["corpus"]["samples_requested"] == 100
