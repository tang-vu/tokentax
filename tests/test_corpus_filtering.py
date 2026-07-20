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


def test_rejects_pairs_containing_markup():
    # Crawl leftovers land asymmetrically: in OPUS-100's Khmer portion they
    # appear in 39% of target sentences and none of the English ones, which
    # would add tokens to every ratio's numerator only.
    english = "How are track ratings determined in this system?"
    assert not corpus.is_usable(english, "Cau tra loi day &#160; roi.")
    assert not corpus.is_usable(english, "Cau tra loi day & # 160; roi.")
    assert not corpus.is_usable(english, "Cau tra loi &nbsp; day roi.")
    assert not corpus.is_usable(english, "Cau tra loi <br> day roi.")
    assert not corpus.is_usable(english, "Xem tai https://example.com nhe.")
    assert not corpus.is_usable(english + " &amp; more", "Cau tra loi day roi.")


def test_accepts_ordinary_punctuation_that_resembles_markup():
    english = "The result was better than expected for the whole team."
    assert corpus.is_usable(english, "Ket qua tot hon du kien <thật> cho ca doi.")
    assert corpus.is_usable(english, "Chi phi tang 5 & 6 phan tram trong nam nay.")


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


def test_resolve_accepts_a_region_name():
    african = corpus.resolve(["Africa"])
    assert african, "Africa should select at least one language"
    assert all(lang.region == "Africa" for lang in african)
    assert "am" in {lang.code for lang in african}


def test_resolve_region_is_case_insensitive():
    assert corpus.resolve(["africa"]) == corpus.resolve(["Africa"])


def test_resolve_mixes_codes_and_regions():
    selected = corpus.resolve(["vi", "Africa"])
    codes = {lang.code for lang in selected}
    assert "vi" in codes
    assert "yo" in codes


def test_every_language_has_a_distinct_code():
    codes = [lang.code for lang in corpus.LANGUAGES]
    assert len(codes) == len(set(codes))


def test_load_pairs_rejects_unknown_language():
    with pytest.raises(KeyError):
        corpus.load_pairs("klingon", 10)


def test_fallback_prefers_held_out_splits():
    assert corpus._fallback_split(["train", "test", "validation"], "en-vi") == "test"
    assert corpus._fallback_split(["train", "validation"], "en-vi") == "validation"


def test_fallback_accepts_train_only_configs():
    # Low-resource pairs often ship train only. Dropping them would bias the
    # benchmark toward well-resourced languages — the exact bias it measures.
    assert corpus._fallback_split(["train"], "en-hy") == "train"


def test_fallback_raises_when_no_split_is_usable():
    with pytest.raises(RuntimeError):
        corpus._fallback_split([], "en-xx")
