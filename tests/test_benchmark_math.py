"""Tests for the measurement math, using deterministic fake tokenizers.

No network access is required: encoders here are plain functions, which is the
same interface the real tokenizer backends expose.
"""

import pytest

from tokentax.benchmark import measure, percentile
from tokentax.results import Measurement
from tokentax.corpus import Language, Pair
from tokentax.tokenizer_registry import Encoding, TokenizerSpec, supports

VIETNAMESE = Language("vi", "Vietnamese", "Latin", "SE Asia")
SPEC = TokenizerSpec(
    key="fake", label="Fake", backend="hf", ref="fake/fake", family="Test"
)


def char_encoder(unknown_per_call: int = 0):
    """One token per character, so expected counts are obvious by inspection."""

    def encode(text: str) -> Encoding:
        return Encoding(tokens=len(text), unknown=unknown_per_call)

    return encode


def test_tax_is_ratio_of_totals_not_mean_of_ratios():
    # Aggregate weighting matters: the long pair should dominate.
    pairs = [Pair(english="ab", target="abcd"), Pair(english="a" * 10, target="a" * 10)]
    result = measure(SPEC, VIETNAMESE, pairs, char_encoder())
    # totals: english 12, target 14 -> 14/12
    assert result.english_tokens == 12
    assert result.target_tokens == 14
    assert result.tax == pytest.approx(14 / 12, abs=1e-4)
    # mean of per-sentence ratios would be (2.0 + 1.0)/2 = 1.5, which differs.
    assert result.tax != pytest.approx(1.5, abs=1e-4)


def test_median_ratio_reported_alongside_aggregate():
    pairs = [
        Pair(english="ab", target="abcd"),  # 2.0
        Pair(english="ab", target="ab"),  # 1.0
        Pair(english="ab", target="abc"),  # 1.5
    ]
    result = measure(SPEC, VIETNAMESE, pairs, char_encoder())
    assert result.median_ratio == pytest.approx(1.5, abs=1e-4)


def test_pairs_counted_excludes_unusable_rows():
    pairs = [Pair(english="", target="abc"), Pair(english="ab", target="abcd")]
    result = measure(SPEC, VIETNAMESE, pairs, char_encoder())
    # The empty English side cannot form a ratio and is dropped entirely.
    assert result.pairs == 1
    assert result.english_tokens == 2


def test_all_unusable_pairs_raises():
    with pytest.raises(ValueError):
        measure(SPEC, VIETNAMESE, [Pair(english="", target="abc")], char_encoder())


def test_empty_pair_list_raises():
    with pytest.raises(ValueError):
        measure(SPEC, VIETNAMESE, [], char_encoder())


def test_unknown_tokens_flag_measurement_as_lossy():
    pairs = [Pair(english="abcdefghij", target="abcdefghij")] * 5
    clean = measure(SPEC, VIETNAMESE, pairs, char_encoder(unknown_per_call=0))
    assert clean.unknown_rate == 0.0
    assert clean.lossy is False

    # 3 unknown tokens per 10-token target is far above the 1% threshold.
    degraded = measure(SPEC, VIETNAMESE, pairs, char_encoder(unknown_per_call=3))
    assert degraded.unknown_rate == pytest.approx(0.3, abs=1e-4)
    assert degraded.lossy is True


def test_tokens_per_char_uses_target_side():
    pairs = [Pair(english="abcd", target="xyz")]
    result = measure(SPEC, VIETNAMESE, pairs, char_encoder())
    assert result.target_tokens_per_char == pytest.approx(1.0, abs=1e-4)


def test_measurement_carries_identifying_labels():
    result = measure(SPEC, VIETNAMESE, [Pair(english="ab", target="abc")], char_encoder())
    assert isinstance(result, Measurement)
    assert result.tokenizer == "fake"
    assert result.language == "vi"
    assert result.language_name == "Vietnamese"


@pytest.mark.parametrize(
    "fraction,expected",
    [(0.0, 1.0), (0.5, 5.0), (0.9, 9.0), (1.0, 10.0)],
)
def test_percentile_nearest_rank(fraction, expected):
    ordered = [float(n) for n in range(1, 11)]
    assert percentile(ordered, fraction) == expected


def test_percentile_of_empty_list_raises():
    with pytest.raises(ValueError):
        percentile([], 0.5)


def test_monolingual_tokenizer_only_supports_its_language():
    phobert = TokenizerSpec(
        key="phobert",
        label="PhoBERT",
        backend="hf",
        ref="vinai/phobert-base-v2",
        family="VinAI",
        languages=("vi",),
    )
    assert supports(phobert, "vi")
    assert not supports(phobert, "th")
    # A tokenizer with no declared languages applies everywhere.
    assert supports(SPEC, "th")
