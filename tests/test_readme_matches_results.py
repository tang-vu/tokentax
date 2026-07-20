"""Guard the README's numeric claims against the committed results.

A benchmark README drifts the moment results are regenerated, and a stale
figure in the one file everybody reads is worse than no figure at all. Every
number asserted in prose is listed here and checked against
``results/token-tax.json``.

These tests skip when results are absent, so a fresh clone can still run the
suite offline before producing any.
"""

import json
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "token-tax.json"
README = ROOT / "README.md"


@pytest.fixture(scope="module")
def data():
    if not RESULTS.exists():
        pytest.skip("no committed results to check against")
    return json.loads(RESULTS.read_text(encoding="utf-8"))["measurements"]


@pytest.fixture(scope="module")
def readme():
    return README.read_text(encoding="utf-8")


def by_language(data, name):
    return [m for m in data if m["language_name"] == name]


def deployable(rows):
    """Cells eligible for a "which should I pick" claim."""
    return [m for m in rows if not m["lossy"] and not m["legacy"]]


def tax(data, language, tokenizer):
    for m in data:
        if m["language_name"] == language and m["tokenizer"] == tokenizer:
            return m["tax"]
    raise AssertionError(f"no measurement for {language}/{tokenizer}")


def test_language_and_tokenizer_counts(data, readme):
    languages = {m["language_name"] for m in data}
    tokenizers = {m["tokenizer"] for m in data}
    assert f"{len(languages)} languages" in readme
    assert f"{len(tokenizers)} tokenizers" in readme


@pytest.mark.parametrize(
    "language,tokenizer,claimed",
    [
        ("Burmese", "sea-lion-v3", 9.28),
        ("Burmese", "llama3", 9.28),
        ("Khmer", "sea-lion-v3", 7.50),
        ("Malayalam", "bloom", 1.20),
        ("Malayalam", "mistral-v3", 8.77),
        ("Punjabi", "mistral-v3", 8.93),
        ("Punjabi", "gpt2", 6.42),
        ("Vietnamese", "mistral-v3", 2.25),
        ("Vietnamese", "cl100k", 1.93),
        ("Vietnamese", "bloom", 1.04),
        ("Vietnamese", "gemma3", 1.08),
        ("Vietnamese", "phobert", 0.76),
        ("Amharic", "gemma3", 1.98),
        ("Burmese", "gemma3", 2.10),
        ("Sinhala", "gemma3", 1.80),
    ],
)
def test_quoted_figure_matches_results(data, readme, language, tokenizer, claimed):
    assert round(tax(data, language, tokenizer), 2) == claimed
    assert f"{claimed:.2f}x" in readme


def test_malayalam_spread_claim(data, readme):
    rows = deployable(by_language(data, "Malayalam"))
    spread = max(m["tax"] for m in rows) / min(m["tax"] for m in rows)
    assert round(spread, 1) == 7.3
    assert "**7.3x**" in readme


def test_languages_claimed_to_have_spreads_above_five(data):
    for language in ("Punjabi", "Gujarati", "Kannada", "Telugu", "Tamil"):
        rows = deployable(by_language(data, language))
        spread = max(m["tax"] for m in rows) / min(m["tax"] for m in rows)
        assert spread > 5, f"{language} spread fell to {spread:.1f}"


def test_cheapest_tokenizer_counts(data, readme):
    languages = {m["language_name"] for m in data}
    counts = Counter(
        min(deployable(by_language(data, lang)), key=lambda m: m["tax"])["tokenizer"]
        for lang in languages
    )
    assert counts["bloom"] == 19
    assert counts["gemma3"] == 12
    assert counts["o200k"] == 8
    assert counts["gemma2"] == 7
    for claim in ("cheapest for 19 of 48", "Gemma 3 is cheapest for 12"):
        assert claim in readme


def test_most_expensive_tokenizer_counts(data, readme):
    languages = {m["language_name"] for m in data}
    counts = Counter(
        max(deployable(by_language(data, lang)), key=lambda m: m["tax"])["tokenizer"]
        for lang in languages
    )
    assert counts["mistral-v3"] == 17 and counts["cl100k"] == 17
    assert counts["bloom"] == 8
    assert "each worst for 17" in readme


def test_gpt2_is_last_place_for_all_but_two_languages(data, readme):
    languages = {m["language_name"] for m in data}
    exceptions = {
        lang
        for lang in languages
        if max(by_language(data, lang), key=lambda m: m["tax"])["tokenizer"] != "gpt2"
    }
    assert exceptions == {"Punjabi", "Armenian"}
    assert "46 of 48" in readme


def test_sea_lion_matches_llama3_everywhere(data):
    """SEA-LION v3 reuses Llama 3's content vocabulary, so taxes must agree.

    If this ever fails, SEA-LION shipped a real tokenizer change and the
    README's claim about it needs rewriting.
    """
    llama = {m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "llama3"}
    sea = {
        m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "sea-lion-v3"
    }
    assert llama and llama == sea


def test_languages_claimed_cheaper_than_english(data, readme):
    for language in ("Chinese", "Indonesian", "Malay"):
        rows = [
            m
            for m in deployable(by_language(data, language))
            if m["tokenizer"] != "phobert"
        ]
        assert min(m["tax"] for m in rows) < 1.0, language
    assert "dip below\n1.00x" in readme or "dip below 1.00x" in readme


@pytest.mark.parametrize(
    "language,claimed", [("Armenian", 4.5), ("Malayalam", 4.2), ("Kannada", 4.1)]
)
def test_cl100k_to_o200k_improvement(data, language, claimed):
    ratio = tax(data, language, "cl100k") / tax(data, language, "o200k")
    assert round(ratio, 1) == claimed


def test_burmese_effective_context_claim(data, readme):
    worst = max(m["tax"] for m in deployable(by_language(data, "Burmese")))
    assert round(128_000 / worst / 1000) == 14
    assert "~14k tokens" in readme


@pytest.mark.parametrize(
    "language,claimed", [("Kurdish", 3.14), ("Yoruba", 2.98), ("Khmer", 2.75)]
)
def test_claimed_floors(data, readme, language, claimed):
    floor = min(m["tax"] for m in deployable(by_language(data, language)))
    assert round(floor, 2) == claimed
    assert f"{claimed:.2f}x" in readme
