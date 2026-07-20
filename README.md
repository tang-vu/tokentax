# tokentax

**How much extra do you pay to prompt an LLM in your own language?**

Same sentence, same meaning, different language — and wildly different token
counts. `tokentax` measures that gap across LLM tokenizers using a
human-translated parallel corpus, so the only variable is the tokenizer.

**48 languages, 23 writing systems, 22 tokenizers.** Runs on a laptop: no GPU,
no model weights, no API keys — tokenizers only.

📊 **[Interactive results →](https://tang-vu.github.io/tokentax/)**

[![Token tax heatmap](docs/token-tax-heatmap.png)](https://tang-vu.github.io/tokentax/)

## What the data says

**Building for a language beats building big.** Aya 101, explicitly trained for
101 languages, is the cheapest option for **28 of 48** languages — more than
every other tokenizer combined. It does this at 250k vocabulary entries, the
same size as BLOOM's, and it wins on exactly the languages everyone else
struggles with: Khmer 1.38x, Burmese 1.38x, Sinhala 1.25x, Amharic 1.50x.
Coverage is a choice, not a budget.

**Narrowing a model's language list has a measurable price.** Cohere's Aya 101
targets 101 languages; its successor Aya Expanse targets 23. Expanse's 255k
vocabulary — *larger* than Aya 101's 250k — contains **zero** entries in Tamil
script, so Tamil falls back to raw bytes: 1.34x becomes 6.10x. Malayalam 1.17x →
7.32x, Khmer 1.38x → 7.46x. Aya 101 is the cheaper tokenizer on **43 of 48**
languages here; Expanse wins only on Vietnamese, Portuguese, French, Spanish,
and Italian. Vocabulary budget is not the constraint — allocation is.

**A regional model can ship the tokenizer it was supposed to fix.** Llama-SEA-LION
v3 is built for Southeast Asia by continued pretraining on Llama 3. Its Burmese
and Khmer costs are *identical to Llama 3's*, because its content vocabulary is
byte-for-byte Llama 3's — the only differences are three special tokens. The
weights learned Southeast Asian languages; the tokenizer never did. Cohere's
Command A and Aya Expanse are likewise identical on all 48 languages — one
vocabulary, two products.

**Fixing one script can break another.** Mistral replaced its 32k vocabulary
with the 131k Tekken, and for Indic scripts it worked: Malayalam fell from 8.77x
to 2.33x, Punjabi 9.02x to 2.79x. Khmer went the other way — 5.08x to **11.66x**,
the highest tax anywhere in this benchmark, and level with GPT-2's 11.57x. Take
one aligned pair of equal length:

> *He won't be able to escape from there without a miracle, will he?*
> — 16 tokens in English, **164** on Tekken, 40 on GPT-4o, 25 on Aya 101.

**A 2025 tokenizer can be worse than a 2019 one.** GPT-2 is last place for 45 of
48 languages. The three exceptions — Khmer, Punjabi, Armenian — are all beaten
to last place by tokenizers shipping today.

**There is no universal winner.** Aya 101 is cheapest for 28 languages, BLOOM
for 16 — and BLOOM is the *most expensive* for 8 others. Mistral v0.3 is worst
for 17, cl100k for 10, GLM-4.5 for 6. Pick by your language, not by reputation.

**Rebuilding the vocabulary works.** Between OpenAI's cl100k and o200k, the same
content got 4.5x cheaper in Armenian, 4.2x in Malayalam, 4.1x in Kannada. This
is a solvable problem, and vendors solve it when they choose to.

**A few languages beat English.** Chinese (0.78x), Indonesian (0.92x), and Malay
(0.98x) all dip below parity on their best tokenizer. Dense scripts win when the
vocabulary covers them.

**Vietnamese**, for the curious: 2.25x on Mistral v0.3 and 1.93x on cl100k, down
to 1.04x on BLOOM and 1.12x on Llama 4. Notably Aya 101, which dominates
elsewhere, manages only 1.53x here — no tokenizer is good at everything. PhoBERT,
trained only on Vietnamese, reaches 0.76x; you cannot bolt it onto a general
model, but it shows the headroom the multilingual tokenizers leave on the table.

Full matrix, per-tokenizer detail, effective-context tables:
[`results/token-tax.md`](results/token-tax.md) ·
[raw JSON](results/token-tax.json)

## Does it replicate?

Everything above is measured on OPUS-100, which is crawled text. A quirk of one
dataset can bias every figure derived from it — this benchmark already found one
such quirk in its own data. So the whole run was repeated against
[WMT24++](https://huggingface.co/datasets/google/wmt24pp): professional human
translation, different domain, **no text in common**.

Over the 31 languages both corpora cover:

- the cheapest tokenizer agrees for **27 of 31** languages
- the most expensive agrees for **26 of 31**
- median drift in absolute tax: **12%**

The headline findings hold on independent text. Aya 101 versus Aya Expanse on
Tamil is 1.34x/6.10x on crawled text and 1.32x/6.43x on translated text; Tekken's
Malayalam improvement is 8.77x → 2.33x and 10.43x → 2.50x. The four ranking
disagreements are all between tokenizers within a few percent of each other.

**Khmer is not in WMT24++**, so the single most extreme finding in this
benchmark — Tekken at 11.66x — is the one that could not be cross-checked. Treat
it as the least confirmed number here.

Full comparison: [`docs/cross-check-against-wmt24pp.md`](docs/cross-check-against-wmt24pp.md).
Reproduce with `tokentax bench --source wmt24pp`.

## Why it matters

Token tax compounds into three real costs:

- **Bill.** APIs charge per token. A 2x tax is a 2x invoice for identical work.
- **Context.** A nominal 128k window holds only ~11k tokens' worth of English
  content when you write Khmer at 11.66x.
- **Latency.** More tokens per request means slower first token and slower
  generation.

## What does *your* text cost?

```console
$ tokentax check "Chính phủ vừa ban hành nghị định mới về quản lý thuế điện tử."

61 characters, 14 whitespace-separated words

  BLOOM                             15 tokens    1.00x
  Qwen3                             16 tokens    1.07x
  Gemma 3                           16 tokens    1.07x
  GPT-4o (o200k)                    17 tokens    1.13x
  Mistral Nemo (Tekken)             17 tokens    1.13x
  GPT-3.5 / GPT-4 (cl100k)          32 tokens    2.13x
  Mistral 7B v0.3                   40 tokens    2.67x

Mistral 7B v0.3 costs 2.7x more than BLOOM for this text.
```

Works on a file too: `tokentax check --file prompt.txt`.

## Usage

```bash
pip install -e .

tokentax check "your text"             # what your own prompt costs
tokentax list                          # tokenizers, languages, regions
tokentax bench                         # everything, 500 pairs per language
tokentax bench --languages vi,th,ta    # specific languages
tokentax bench --languages Africa      # or a whole region
tokentax bench --tokenizers o200k,qwen3 --samples 1000
tokentax render                        # rebuild reports from existing JSON
```

`bench` writes `token-tax.md`, `token-tax.json`, and `index.html` to `--out`
(default `results/`).

## How it stays honest

Benchmarks are easy to accidentally rig. Five things guard against it:

**Aligned translations.** Every ratio compares the same sentence in both
languages, from [OPUS-100](https://huggingface.co/datasets/Helsinki-NLP/opus-100).
Counting tokens on unrelated texts would measure the texts, not the tokenizer.

**Crawl markup is removed, because it lands unevenly.** OPUS-100 is scraped, and
leftover HTML entities appeared in 39% of the Khmer target sentences against 0%
of their English counterparts. Markup on one side only adds tokens to the
numerator of every ratio and none to the denominator; leaving it in inflated
Khmer's tax by 4% and Gemma 3's Khmer figure by 10%. Pairs carrying markup on
either side are dropped, which is why some languages report fewer than the
requested pairs — the report names them.

**Lossy encodings are disqualified.** A tokenizer that cannot represent a script
emits `<unk>` and posts a token count for text it has already mangled. PhoBERT
scores 2.12x on Thai — mid-table, and meaningless, because 3.5% of those tokens
are `<unk>` and the Thai is disintegrating into characters. Cells above 1%
unknown tokens are flagged and excluded from rankings.

**Historical baselines don't pad the rankings.** GPT-2 is the worst option for
45 of 48 languages. Leaving it in the "most expensive" column would be true and
useless, so it appears in the matrix as a reference point only — which is also
how the three exceptions become visible.

**Low-resource languages aren't quietly dropped.** Some OPUS-100 pairs ship no
held-out split. Skipping them would bias the benchmark toward well-resourced
languages — the exact bias it exists to measure — so those languages fall back
to another split and every report names them.

Full methodology and limitations:
[`docs/methodology-and-limitations.md`](docs/methodology-and-limitations.md).

Tokenizer efficiency is **not** model quality. A cheap tokenizer attached to a
weak model is still a bad choice.

## Adding a tokenizer or language

Both are one entry each — no other code changes.

A tokenizer, in `src/tokentax/tokenizer_registry.py`:

```python
TokenizerSpec(
    key="my-model",
    label="My Model",
    backend="hf",                  # or "tiktoken"
    ref="org/my-model",            # HF repo id, or tiktoken encoding name
    family="Org",
    vocab_note="64k BPE",
    # languages=("vi",)            # only for monolingual tokenizers
)
```

A language, in `src/tokentax/languages.py` — any of OPUS-100's ~100 languages:

```python
Language("so", "Somali", "Latin", "Africa")
```

Then `tokentax bench --languages so --tokenizers my-model` and open a PR.
Results for underrepresented languages are especially welcome — the gaps above
are worst exactly where measurement is thinnest.

## Development

```bash
pip install -e ".[dev]"
pytest
```

The suite uses fake tokenizers throughout, so it runs offline in under a second.

## License

MIT
