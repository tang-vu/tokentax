# tokentax

**How much extra do you pay to prompt an LLM in your own language?**

Same sentence, same meaning, different language — and wildly different token
counts. `tokentax` measures that gap across LLM tokenizers using a
human-translated parallel corpus, so the only variable is the tokenizer.

**48 languages, 23 writing systems, 13 tokenizers.** Runs on a laptop: no GPU,
no model weights, no API keys — tokenizers only.

📊 **[Interactive results →](https://tang-vu.github.io/tokentax/)**

[![Token tax heatmap](docs/token-tax-heatmap.png)](https://tang-vu.github.io/tokentax/)

## What the data says

**A regional model can ship the tokenizer it was supposed to fix.** Llama-SEA-LION
v3 is built for Southeast Asia by continued pretraining on Llama 3. Its
Burmese and Khmer token costs — 9.28x and 7.50x — are *identical to Llama 3's*,
because its content vocabulary is byte-for-byte Llama 3's. The only differences
are three special tokens. The weights learned Southeast Asian languages; the
tokenizer never did, so users still pay Llama 3's tax on every request.

**The gap between tokenizers is bigger than most people's entire optimisation
budget.** Malayalam costs 1.20x on BLOOM and 8.77x on Mistral 7B v0.3 — a
**7.3x** difference for identical text, decided entirely by which tokenizer you
picked. Punjabi, Gujarati, Kannada, Telugu, and Tamil all show gaps above 5x.

**A 2024 tokenizer can be worse than a 2019 one.** Mistral 7B v0.3 costs 8.93x
for Punjabi; GPT-2, English-only and six years older, costs 6.42x. Punjabi and
Armenian are the only two languages of 48 where anything beats GPT-2 to last
place — and in both cases it is a currently shipping model.

**Some languages have no good option.** Kurdish's cheapest tokenizer still costs
3.14x, Yoruba 2.98x, Khmer 2.75x. For these, switching vendors does not rescue
you — nobody has built a vocabulary that covers them well.

**Newer vocabularies are closing the gap.** Gemma 3 is the cheapest option for
12 of 48 languages and improves on every previously measured tokenizer for
Amharic (2.90x → 1.98x), Burmese (2.64x → 2.10x), and Sinhala (2.11x → 1.80x).
The languages that were worst served are exactly where the recent gains land.

**There is no universal winner.** BLOOM is cheapest for 19 of 48 languages and
the *most expensive* for 8 others. Gemma 3 is cheapest for 12, GPT-4o for 8,
Gemma 2 for 7. Mistral v0.3 and cl100k are each worst for 17. Pick by your
language, not by reputation.

**Rebuilding the vocabulary works — dramatically.** Between OpenAI's cl100k and
o200k, the same content got 4.5x cheaper in Armenian, 4.2x in Malayalam, 4.1x in
Kannada. This is a solvable problem, and vendors solve it when they choose to.

**A few languages beat English.** Chinese, Indonesian, and Malay all dip below
1.00x on their best tokenizer. Dense scripts win when the vocabulary covers them.

**Vietnamese**, for the curious: 2.25x on Mistral and 1.93x on cl100k, down to
1.04x on BLOOM and 1.08x on Gemma 3. PhoBERT, trained only on Vietnamese,
reaches 0.76x — you cannot bolt it onto a general model, but it shows how much
headroom the multilingual tokenizers leave on the table.

Full matrix, per-tokenizer detail, effective-context tables:
[`results/token-tax.md`](results/token-tax.md) ·
[raw JSON](results/token-tax.json)

## Why it matters

Token tax compounds into three real costs:

- **Bill.** APIs charge per token. A 2x tax is a 2x invoice for identical work.
- **Context.** A nominal 128k window holds only ~14k tokens' worth of English
  content when you write Burmese at 9.28x.
- **Latency.** More tokens per request means slower first token and slower
  generation.

## Usage

```bash
pip install -e .

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

Benchmarks are easy to accidentally rig. Four things guard against it:

**Aligned translations.** Every ratio compares the same sentence in both
languages, from [OPUS-100](https://huggingface.co/datasets/Helsinki-NLP/opus-100).
Counting tokens on unrelated texts would measure the texts, not the tokenizer.

**Lossy encodings are disqualified.** A tokenizer that cannot represent a script
emits `<unk>` and posts a token count for text it has already mangled. PhoBERT
scores 2.12x on Thai — mid-table, and meaningless, because 3.5% of those tokens
are `<unk>` and the Thai is disintegrating into characters. Cells above 1%
unknown tokens are flagged and excluded from rankings.

**Historical baselines don't pad the rankings.** GPT-2 is the worst option for
46 of 48 languages. Leaving it in the "most expensive" column would be true and
useless, so it appears in the matrix as a reference point only — which is also
how the two exceptions become visible.

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
