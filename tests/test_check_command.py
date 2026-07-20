"""Tests for the ad-hoc text checker."""

import pytest

from tokentax.check import Count, InputError, format_report, resolve_text


def counts(*pairs):
    return [
        Count(key=k, label=k.upper(), tokens=t, unknown=u) for k, t, u in pairs
    ]


def test_resolve_text_prefers_the_positional_argument():
    assert resolve_text("hello", None) == "hello"


def test_resolve_text_reads_a_file(tmp_path):
    path = tmp_path / "prompt.txt"
    path.write_text("xin chào", encoding="utf-8")
    assert resolve_text(None, path) == "xin chào"


def test_resolve_text_rejects_both_sources(tmp_path):
    path = tmp_path / "prompt.txt"
    path.write_text("hi", encoding="utf-8")
    with pytest.raises(InputError):
        resolve_text("hello", path)


def test_resolve_text_rejects_missing_file(tmp_path):
    with pytest.raises(InputError):
        resolve_text(None, tmp_path / "absent.txt")


def test_resolve_text_rejects_nothing_at_all():
    with pytest.raises(InputError):
        resolve_text(None, None)


def test_resolve_text_rejects_whitespace_only():
    with pytest.raises(InputError):
        resolve_text("   \n\t ", None)


def test_ratios_are_relative_to_the_cheapest():
    report = format_report("abc", counts(("a", 10, 0), ("b", 20, 0)), {})
    assert "1.00x" in report
    assert "2.00x" in report
    assert "2.0x more" in report


def test_lossy_tokenizer_does_not_set_the_baseline():
    # A tokenizer that dropped characters would otherwise define a baseline
    # nothing else can honestly match, deflating every other ratio.
    report = format_report(
        "abc", counts(("broken", 5, 3), ("good", 10, 0), ("worse", 20, 0)), {}
    )
    assert "⚠ 3 unknown" in report
    assert "2.00x" in report  # worse vs good, not vs broken
    assert "4.00x" not in report


def test_single_tokenizer_omits_the_comparison_line():
    report = format_report("abc", counts(("only", 10, 0)), {})
    assert "more than" not in report


def test_load_failures_are_listed():
    report = format_report("abc", counts(("a", 10, 0)), {"gated": "401 error"})
    assert "Could not load:" in report
    assert "401 error" in report


def test_empty_counts_reports_cleanly():
    assert "no tokenizers" in format_report("abc", [], {})


def test_character_and_word_totals_are_reported():
    report = format_report("one two three", counts(("a", 3, 0)), {})
    assert "13 characters" in report
    assert "3 whitespace-separated words" in report
