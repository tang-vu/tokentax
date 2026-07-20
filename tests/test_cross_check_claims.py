"""Guard the README's replication claims against both committed runs.

The cross-check is the project's strongest credibility claim, so its figures
get the same treatment as the headline ones: asserted against the data, not
trusted to stay true.
"""

import json
import re
from pathlib import Path

import pytest

from tokentax.cross_check import compare
from tokentax.results import BenchmarkRun

ROOT = Path(__file__).resolve().parents[1]
BASELINE = ROOT / "results" / "token-tax.json"
SECOND = ROOT / "results" / "wmt24pp" / "token-tax.json"
README = ROOT / "README.md"


def load(path):
    return BenchmarkRun.from_dict(json.loads(path.read_text(encoding="utf-8")))


@pytest.fixture(scope="module")
def rows():
    if not (BASELINE.exists() and SECOND.exists()):
        pytest.skip("both runs are needed for the cross-check")
    return compare(load(BASELINE), load(SECOND))


@pytest.fixture(scope="module")
def readme():
    return re.sub(r"\s+", " ", README.read_text(encoding="utf-8"))


def test_shared_language_count(rows, readme):
    assert len(rows) == 31
    assert "31 languages both corpora cover" in readme


def test_ranking_agreement_counts(rows, readme):
    assert sum(1 for r in rows if r.cheapest_agrees) == 27
    assert sum(1 for r in rows if r.dearest_agrees) == 26
    assert "**27 of 31**" in readme
    assert "**26 of 31**" in readme


def test_disagreements_are_between_near_tied_tokenizers(rows):
    """The README waves the four disagreements off; check that is fair.

    A ranking flip between tokenizers that differ by a wide margin would be a
    real contradiction, not corpus noise.
    """
    baseline = {
        (m.language_name, m.tokenizer): m.tax for m in load(BASELINE).measurements
    }
    for row in rows:
        if row.cheapest_agrees:
            continue
        winner = baseline[(row.language, row.cheapest_a)]
        challenger = baseline[(row.language, row.cheapest_b)]
        assert challenger / winner < 1.35, (
            f"{row.language}: {row.cheapest_a} and {row.cheapest_b} are not close"
        )


def test_khmer_is_absent_from_the_second_corpus(rows, readme):
    """The README says so explicitly; if that changes, the caveat must go."""
    assert "Khmer" not in {r.language for r in rows}
    assert "Khmer is not in WMT24++" in readme


@pytest.mark.parametrize(
    "language,tokenizer,claimed",
    [
        ("Tamil", "aya-101", 1.32),
        ("Tamil", "aya-expanse", 6.43),
        ("Malayalam", "mistral-v3", 10.43),
        ("Malayalam", "mistral-nemo", 2.50),
    ],
)
def test_quoted_second_corpus_figures(readme, language, tokenizer, claimed):
    run = load(SECOND) if SECOND.exists() else pytest.skip("no second run")
    actual = next(
        m.tax
        for m in run.measurements
        if m.language_name == language and m.tokenizer == tokenizer
    )
    assert round(actual, 2) == claimed
    assert f"{claimed:.2f}x" in readme
