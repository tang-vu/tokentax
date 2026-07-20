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

**Gated repos are skipped by default.** Llama and Gemma tokenizers require
Hugging Face authentication. They are in the registry but excluded unless run
with `--tokenizers all+gated` while authenticated, and their absence is recorded
in the report's `Skipped` section rather than hidden.

**Single corpus.** Every number derives from one dataset. Cross-checking against
FLORES+ or Tatoeba would strengthen the conclusions; FLORES+ is currently gated
on the Hub, which is why it is not used here.
