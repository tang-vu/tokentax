# tokentax

**How much extra do you pay to prompt an LLM in your own language?**

Same sentence, same meaning, different language — and wildly different token
counts. `tokentax` measures that gap across LLM tokenizers using a
human-translated parallel corpus, so the only variable is the tokenizer.

Runs on a laptop. No GPU, no model weights, no API keys — tokenizers only.

```bash
pip install -e .
tokentax bench --languages vi,ta,th --samples 500
```

## The headline

Tokens per unit of meaning, relative to English (`1.00x` = parity):

| Language | Cheapest tokenizer | | Most expensive | | You overpay |
|---|---|---:|---|---:|---:|
| Tamil | BLOOM | 1.42x | Llama-SEA-LION v3 | 7.47x | **5.3x** |
| Hindi | BLOOM | 1.29x | GPT-3.5 / GPT-4 | 4.38x | **3.4x** |
| Arabic | BLOOM | 1.01x | Mistral 7B v0.3 | 2.99x | **3.0x** |
| Vietnamese | PhoBERT *(VN-only)* | 0.76x | Mistral 7B v0.3 | 2.25x | **2.9x** |
| Persian | Llama-SEA-LION v3 | 1.52x | Mistral 7B v0.3 | 3.44x | **2.3x** |
| Thai | GPT-4o | 1.47x | BLOOM | 3.24x | **2.2x** |
| Chinese | BLOOM | 0.78x | GPT-3.5 / GPT-4 | 1.68x | **2.1x** |
| Korean | Llama-SEA-LION v3 | 1.16x | BLOOM | 2.10x | **1.8x** |
| Japanese | Qwen2.5 | 1.08x | GPT-3.5 / GPT-4 | 1.66x | **1.5x** |
| Spanish | BLOOM | 1.09x | Mistral 7B v0.3 | 1.41x | **1.3x** |

Full 15-language matrix, per-tokenizer detail, and effective-context tables:
[`results/token-tax.md`](results/token-tax.md). Raw numbers:
[`results/token-tax.json`](results/token-tax.json).

## What the data says

**A Tamil speaker pays ~6x for the same content on most tokenizers shipping
today.** Not a 2019 artifact — Qwen2.5, Qwen3, and Llama-SEA-LION all land
between 5.97x and 7.47x for Tamil. Only BLOOM (1.42x) and GPT-4o (2.05x) are
anywhere near parity.

**There is no universal winner.** BLOOM is the cheapest option for seven of
fifteen languages and the *most expensive* for Thai, Russian, Korean, and
German. Picking a tokenizer by reputation instead of by your language is how
you end up on the wrong side of a 2x gap.

**Some languages are cheaper than English.** Chinese on BLOOM is 0.78x,
Indonesian 0.92x, Arabic 1.01x. Dense scripts win when the vocabulary covers
them.

**Vocabulary size is not the story.** Mistral's 32k vocabulary is the most
expensive choice for seven languages. BLOOM's 250k and GPT-4o's 200k do well —
but so does SEA-LION on Korean and Turkish with a smaller extended vocabulary.
What matters is whether *your* language was in scope when the vocabulary was
built.

**Rebuilding the vocabulary works.** Across the OpenAI generations, the same
content went from 7.47x to 2.05x for Tamil and 1.93x to 1.25x for Vietnamese.
This is a solvable problem, and vendors solve it when they choose to.

**The ceiling is lower than any general tokenizer reaches.** PhoBERT, trained
only on Vietnamese, encodes Vietnamese in *fewer* tokens than English (0.76x).
You cannot bolt it onto a general LLM, but it shows how much headroom the
multilingual tokenizers still leave on the table.

## Why this is worth measuring

Token tax compounds into three real costs:

- **Bill.** APIs charge per token. A 2x tax is a 2x invoice for identical work.
- **Context.** A nominal 128k window holds only ~17k tokens' worth of English
  content when you write Tamil on the tokenizer that taxes it at 7.47x.
- **Latency.** More tokens per request means more time to first token and more
  to generate.

## Usage

```bash
tokentax list                          # available tokenizers and languages
tokentax bench                         # everything, 500 pairs per language
tokentax bench --languages vi,th,ta    # specific languages
tokentax bench --tokenizers o200k,qwen3 --samples 1000
tokentax bench --tokenizers all+gated  # include Llama/Gemma (needs HF login)
```

Writes `token-tax.md` and `token-tax.json` to `--out` (default `results/`).

## How it stays honest

Benchmarks are easy to accidentally rig. Three things guard against it:

**Aligned translations.** Every ratio compares the same sentence in both
languages, drawn from [OPUS-100](https://huggingface.co/datasets/Helsinki-NLP/opus-100).
Counting tokens on unrelated texts would measure the texts, not the tokenizer.

**Lossy encodings are disqualified.** A tokenizer that cannot represent a
script emits `<unk>` and posts a token count for text it has already mangled.
PhoBERT scores 2.12x on Thai — mid-table, and meaningless, because 3.5% of
those tokens are `<unk>` and the Thai is falling apart into characters. Cells
above 1% unknown tokens are flagged `⚠` and excluded from rankings, and
monolingual tokenizers are only measured on the languages they target.

**Historical baselines don't pad the rankings.** GPT-2 is the worst option for
all fifteen languages. Leaving it in the "most expensive" column would be true
and useless, so it appears in the matrix as a reference point only.

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

A language, in `src/tokentax/corpus.py` — any of OPUS-100's ~100 languages:

```python
Language("ms", "Malay", "Latin")
```

Then `tokentax bench --languages ms --tokenizers my-model` and open a PR with
the result. Results for underrepresented languages are especially welcome.

## Development

```bash
pip install -e ".[dev]"
pytest
```

The suite uses fake tokenizers throughout, so it runs offline in under a second.

## License

MIT
