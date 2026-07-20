# Methodology and limitations

## What is measured

For a language `L` and tokenizer `T`, the **token tax** is:

```
tax(L, T) = total_tokens(T, L_sentences) / total_tokens(T, English_sentences)
```

over aligned sentence pairs — the same content expressed in both languages. A
tax of `2.00x` means encoding that content in `L` consumes twice as many tokens
as encoding it in English, which translates directly into twice the API cost and
half the usable context window.

English is the baseline by construction and always scores `1.00x`.

## Why a parallel corpus

Counting tokens on unrelated Vietnamese and English text measures whatever those
texts happen to say, not the tokenizer. Aligned translations hold content
constant so the remaining difference is attributable to the tokenizer's
vocabulary.

The corpus is [OPUS-100](https://huggingface.co/datasets/Helsinki-NLP/opus-100),
human-translated and covering ~100 languages paired against English.

## Aggregate rather than mean-of-ratios

Tax uses total tokens over total tokens, not the average of per-sentence ratios.
Cost accrues on totals, so long sentences should carry proportionally more
weight. The per-sentence median and p90 appear in the JSON output; a large gap
between aggregate and median indicates a few long sentences dominate.

## Splits

The `test` split is used wherever it exists. A number of low-resource OPUS-100
configs ship only `train`; those languages fall back to `validation`, then
`train`, and the split actually used is recorded per measurement and named in
both reports.

The fallback is deliberate. Restricting the benchmark to languages with a
held-out split would quietly exclude the least-resourced ones — precisely the
group whose token tax is highest and least documented. The cost is that those
rows are not held out and, being noisier crawled text, less precise; they are
marked so readers can weigh them accordingly.

## Filtering

OPUS-100 is crawled data. Before counting, pairs are dropped when:

- the English side is shorter than 25 or longer than 400 characters
- the target side is under 5 characters
- both sides are byte-identical (the row was never translated)
- the character-length ratio falls outside `0.2`–`5.0` (near-certain misalignment)
- the English side duplicates an earlier pair

These thresholds are deliberately loose. They exist to remove junk, not to steer
the result.

## Lossy encodings

A tokenizer that cannot represent a script emits unknown tokens and can post a
*low* token count while destroying the text. PhoBERT on Thai is the clearest
case: it falls back to characters plus `<unk>` and produces a number that looks
competitive but describes mangled input.

Cells where unknown tokens exceed 1% of the target-side total are marked lossy,
flagged with `⚠` in the report, and excluded from best/worst rankings.
Monolingual tokenizers additionally declare the languages they target and are
not measured outside them.

`tiktoken` encodings are byte-level BPE and have no unknown-token failure mode,
so they always report a zero unknown rate.

## Limitations

**Tokenizer efficiency is not model quality.** A tokenizer with a low tax
attached to a weak model is still a bad choice. This benchmark answers "what
will this cost me per unit of meaning", not "which model is better".

**Domain is fixed.** OPUS-100 skews toward subtitles, web text, and
administrative prose. Tax varies by register — informal conversational text
consistently taxes lower than formal or technical writing, because formal
vocabulary is rarer in tokenizer training data. Numbers here should not be read
as universal constants for a language.

**Chat templates are excluded.** Only content tokens are counted. Real requests
also pay for system prompts and template scaffolding, which are usually English
and therefore dilute the measured tax slightly in practice.

**Tokenizer, not model, versions.** Entries are identified by the Hub repo whose
`tokenizer.json` was loaded. Models sharing a vocabulary produce identical
numbers; the registry labels are chosen to make the family clear.

**Some tokenizers come from community mirrors.** Meta's and Google's own
Hugging Face repos are gated behind an access agreement, which would make the
benchmark unreproducible for anyone without accepted terms. Llama 3, Gemma 2,
and Gemma 3 are therefore loaded from public re-uploads, flagged as mirrors in
`tokentax list`.

Vocabulary sizes match the published specifications (Llama 3 at 128,256; Gemma 2
at 256,000), which is a useful consistency check but not a cryptographic one. If
a mirror diverged from the original in some subtler way, this benchmark would
not detect it. Anyone with accepted terms can point those entries at the
official repos and compare.

The `gated` flag remains in the registry so a future gated entry fails with a
clear message rather than an opaque 401.

**Single corpus.** Every number derives from one dataset. Cross-checking against
FLORES+ or Tatoeba would strengthen the conclusions; FLORES+ is currently gated
on the Hub, which is why it is not used here.

**Language coverage is intentionally skewed.** The 48 languages over-represent
non-Latin scripts and under-resourced languages relative to global speaker
counts. Western European languages are present as a control group, not for
balance. Do not read the language list as a ranking of importance.

**Sentence-level, not document-level.** Tax is measured on individual sentences.
Long-document behaviour may differ slightly as a tokenizer's merges get more
opportunities to fire, though the effect is small for BPE.
