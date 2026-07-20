"""Guard the README's numeric claims against the committed results.

A benchmark README drifts the moment results are regenerated, and a stale
figure in the one file everybody reads is worse than no figure at all. Every
number asserted in prose is listed here and checked against
``results/token-tax.json``.

The README fixture collapses whitespace, so assertions survive re-wrapping of
the prose and only fail when the substance changes.

These tests skip when results are absent, so a fresh clone can still run the
suite offline before producing any.
"""

import json
import re
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
    return re.sub(r"\s+", " ", README.read_text(encoding="utf-8"))


def by_language(data, name):
    return [m for m in data if m["language_name"] == name]


def deployable(rows):
    """Cells eligible for a "which should I pick" claim."""
    return [m for m in rows if not m["lossy"] and not m["legacy"]]


def general_purpose(rows):
    """A monolingual tokenizer is not an option for a multilingual model."""
    return [m for m in deployable(rows) if m["tokenizer"] != "phobert"]


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
        ("Khmer", "aya-101", 1.49),
        ("Burmese", "aya-101", 1.38),
        ("Sinhala", "aya-101", 1.25),
        ("Amharic", "aya-101", 1.50),
        ("Tamil", "aya-101", 1.34),
        ("Tamil", "aya-expanse", 6.10),
        ("Malayalam", "aya-101", 1.17),
        ("Malayalam", "aya-expanse", 7.32),
        ("Khmer", "aya-expanse", 7.84),
        ("Malayalam", "mistral-v3", 8.77),
        ("Malayalam", "mistral-nemo", 2.33),
        ("Punjabi", "mistral-v3", 8.93),
        ("Punjabi", "mistral-nemo", 2.77),
        ("Khmer", "mistral-v3", 5.46),
        ("Khmer", "mistral-nemo", 12.08),
        ("Khmer", "gpt2", 11.88),
        ("Vietnamese", "mistral-v3", 2.25),
        ("Vietnamese", "cl100k", 1.93),
        ("Vietnamese", "bloom", 1.04),
        ("Vietnamese", "llama4", 1.12),
        ("Vietnamese", "aya-101", 1.53),
        ("Vietnamese", "phobert", 0.76),
        ("Chinese", "bloom", 0.78),
        ("Indonesian", "bloom", 0.92),
        ("Malay", "bloom", 0.98),
    ],
)
def test_quoted_figure_matches_results(data, readme, language, tokenizer, claimed):
    assert round(tax(data, language, tokenizer), 2) == claimed
    assert f"{claimed:.2f}x" in readme


def test_khmer_is_the_worst_cell_measured(data, readme):
    worst = max(
        (m for m in data if not m["lossy"] and not m["legacy"]),
        key=lambda m: m["tax"],
    )
    assert worst["language_name"] == "Khmer"
    assert worst["tokenizer"] == "mistral-nemo"
    assert "the highest tax anywhere in this benchmark" in readme


def test_tekken_helps_indic_and_hurts_khmer(data, readme):
    """The README's sharpest claim: the same vocabulary swap cut both ways."""
    for language in ("Malayalam", "Punjabi"):
        assert tax(data, language, "mistral-nemo") < tax(data, language, "mistral-v3")
    assert tax(data, "Khmer", "mistral-nemo") > tax(data, "Khmer", "mistral-v3")
    assert tax(data, "Khmer", "mistral-nemo") > tax(data, "Khmer", "gpt2")
    assert "Fixing one script can break another" in readme


def test_cheapest_tokenizer_counts(data, readme):
    languages = {m["language_name"] for m in data}
    counts = Counter(
        min(general_purpose(by_language(data, lang)), key=lambda m: m["tax"])[
            "tokenizer"
        ]
        for lang in languages
    )
    assert counts["aya-101"] == 28
    assert counts["bloom"] == 16
    assert "**28 of 48**" in readme
    assert "cheapest for 28 languages, BLOOM for 16" in readme


def test_most_expensive_tokenizer_counts(data, readme):
    languages = {m["language_name"] for m in data}
    counts = Counter(
        max(general_purpose(by_language(data, lang)), key=lambda m: m["tax"])[
            "tokenizer"
        ]
        for lang in languages
    )
    assert counts["mistral-v3"] == 17
    assert counts["cl100k"] == 10
    assert counts["bloom"] == 8
    assert counts["glm4.5"] == 6
    assert "worst for 17, cl100k for 10, GLM-4.5 for 6" in readme


def test_gpt2_is_last_place_for_all_but_three_languages(data, readme):
    languages = {m["language_name"] for m in data}
    exceptions = {
        lang
        for lang in languages
        if max(by_language(data, lang), key=lambda m: m["tax"])["tokenizer"] != "gpt2"
    }
    assert exceptions == {"Punjabi", "Armenian", "Khmer"}
    assert "45 of 48 languages" in readme


def test_sea_lion_matches_llama3_everywhere(data, readme):
    """SEA-LION v3 reuses Llama 3's content vocabulary, so taxes must agree.

    If this ever fails, SEA-LION shipped a real tokenizer change and the
    README's claim about it needs rewriting.
    """
    llama = {m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "llama3"}
    sea = {
        m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "sea-lion-v3"
    }
    assert llama and llama == sea
    assert "byte-for-byte Llama 3's" in readme


def test_aya_101_beats_its_own_successor_on_most_languages(data, readme):
    """Aya Expanse has the larger vocabulary and the narrower language list."""
    expanse = {
        m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "aya-expanse"
    }
    old = {m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "aya-101"}
    cheaper = [lang for lang in old if old[lang] < expanse[lang]]
    dearer = {lang for lang in old if old[lang] > expanse[lang]}
    assert len(cheaper) == 43
    assert dearer == {
        "Vietnamese",
        "Portuguese",
        "French",
        "Spanish",
        "Italian",
    }
    assert "**43 of 48**" in readme


def test_command_a_matches_aya_expanse_everywhere(data, readme):
    """Two Cohere products, one vocabulary — as with SEA-LION and Llama 3."""
    expanse = {
        m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "aya-expanse"
    }
    command = {
        m["language_name"]: m["tax"] for m in data if m["tokenizer"] == "command-a"
    }
    assert expanse and expanse == command
    assert "one vocabulary, two products" in readme


def test_languages_claimed_cheaper_than_english(data, readme):
    for language in ("Chinese", "Indonesian", "Malay"):
        rows = general_purpose(by_language(data, language))
        assert min(m["tax"] for m in rows) < 1.0, language
    assert "dip below parity" in readme


@pytest.mark.parametrize(
    "language,claimed", [("Armenian", 4.5), ("Malayalam", 4.2), ("Kannada", 4.1)]
)
def test_cl100k_to_o200k_improvement(data, language, claimed):
    ratio = tax(data, language, "cl100k") / tax(data, language, "o200k")
    assert round(ratio, 1) == claimed


def test_khmer_effective_context_claim(data, readme):
    worst = max(m["tax"] for m in general_purpose(by_language(data, "Khmer")))
    assert round(128_000 / worst / 1000) == 11
    assert "~11k tokens" in readme


@pytest.mark.parametrize(
    "language,claimed",
    [("Khmer", 1.49), ("Burmese", 1.38), ("Sinhala", 1.25), ("Amharic", 1.50)],
)
def test_aya_sets_the_floor_for_the_worst_served_languages(data, language, claimed):
    rows = general_purpose(by_language(data, language))
    floor = min(rows, key=lambda m: m["tax"])
    assert round(floor["tax"], 2) == claimed
    assert floor["tokenizer"] == "aya-101"
