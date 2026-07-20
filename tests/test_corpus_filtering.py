"""Tests for corpus alignment filters and language resolution."""

import pytest

from tokentax import corpus


def test_config_name_orders_pair_alphabetically():
    # OPUS-100 names configs as a sorted pair, so the side English lands on
    # depends on the other language's code.
    assert corpus.config_name("vi") == "en-vi"
    assert corpus.config_name("zh") == "en-zh"
    assert corpus.config_name("de") == "de-en"
    assert corpus.config_name("ar") == "ar-en"


def test_usable_pair_accepted():
    english = "The government issued a new decree on tax administration."
    target = "Chinh phu vua ban hanh nghi dinh moi ve quan ly thue."
    assert corpus.is_usable(english, target)


def test_rejects_english_that_is_too_short():
    assert not corpus.is_usable("Hello.", "Xin chao cac ban gan xa.")


def test_rejects_english_that_is_too_long():
    english = "word " * 200
    assert not corpus.is_usable(english, "ngan gon")


def test_rejects_untranslated_row():
    # Identical sides mean the row was copied, not translated.
    text = "This sentence was never actually translated at all."
    assert not corpus.is_usable(text, text)


def test_rejects_misaligned_pair_by_length_ratio():
    english = "A reasonably long English sentence that carries real content."
    assert not corpus.is_usable(english, "ok")  # target far too short
    assert not corpus.is_usable(english, "x" * 5000)  # target far too long


def test_rejects_empty_target():
    assert not corpus.is_usable("A reasonably long English sentence here.", "")


def test_resolve_defaults_to_every_language():
    assert corpus.resolve(None) == list(corpus.LANGUAGES)
    assert corpus.resolve(["all"]) == list(corpus.LANGUAGES)


def test_resolve_selects_requested_languages_in_order():
    selected = corpus.resolve(["th", "vi"])
    assert [lang.code for lang in selected] == ["th", "vi"]


def test_resolve_rejects_unknown_language():
    with pytest.raises(KeyError):
        corpus.resolve(["vi", "klingon"])


def test_load_pairs_rejects_unknown_language():
    with pytest.raises(KeyError):
        corpus.load_pairs("klingon", 10)
