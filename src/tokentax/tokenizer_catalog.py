"""What tokenizers exist, and how to select them.

Separated from the loading code because this file is a data table: adding a
tokenizer should mean adding an entry here and touching nothing else. Loading
lives in :mod:`tokenizer_registry`.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class TokenizerSpec:
    """Static description of one tokenizer entry."""

    key: str
    label: str
    backend: str  # "tiktoken" | "hf"
    ref: str  # encoding name, or HF repo id
    family: str
    vocab_note: str = ""
    gated: bool = False
    # Monolingual tokenizers are only meaningful for the languages they were
    # built for. ``None`` means the tokenizer targets no particular language.
    languages: tuple[str, ...] | None = None
    # Historical reference points. Shown in the matrix so the generational
    # trend is visible, but kept out of "which should I pick" rankings, where
    # a tokenizer nobody deploys would dominate every row.
    legacy: bool = False


# Ordered roughly oldest -> newest so reports read as a timeline.
REGISTRY: tuple[TokenizerSpec, ...] = (
    TokenizerSpec(
        key="gpt2",
        label="GPT-2 (2019)",
        backend="hf",
        ref="gpt2",
        family="OpenAI",
        vocab_note="50k BPE, English-centric",
        legacy=True,
    ),
    TokenizerSpec(
        key="cl100k",
        label="GPT-3.5 / GPT-4 (cl100k)",
        backend="tiktoken",
        ref="cl100k_base",
        family="OpenAI",
        vocab_note="100k BPE",
    ),
    TokenizerSpec(
        key="o200k",
        label="GPT-4o (o200k)",
        backend="tiktoken",
        ref="o200k_base",
        family="OpenAI",
        vocab_note="200k BPE, multilingual rebuild",
    ),
    TokenizerSpec(
        key="mistral-v3",
        label="Mistral 7B v0.3",
        backend="hf",
        ref="mistralai/Mistral-7B-Instruct-v0.3",
        family="Mistral",
        vocab_note="32k SentencePiece",
    ),
    TokenizerSpec(
        key="bloom",
        label="BLOOM",
        backend="hf",
        ref="bigscience/bloom-560m",
        family="BigScience",
        vocab_note="250k, multilingual by design",
    ),
    TokenizerSpec(
        key="llama3",
        label="Llama 3",
        backend="hf",
        ref="NousResearch/Meta-Llama-3-8B",
        family="Meta",
        vocab_note="128k BPE; mirror, verified identical to meta-llama/Meta-Llama-3-8B",
    ),
    TokenizerSpec(
        key="gemma2",
        label="Gemma 2",
        backend="hf",
        ref="unsloth/gemma-2-2b",
        family="Google",
        vocab_note="256k SentencePiece; mirror, verified identical to google/gemma-2-2b",
    ),
    TokenizerSpec(
        key="mistral-nemo",
        label="Mistral Nemo (Tekken)",
        backend="hf",
        ref="mistralai/Mistral-Nemo-Instruct-2407",
        family="Mistral",
        vocab_note="131k Tekken, Mistral's multilingual replacement for the 32k vocab",
    ),
    TokenizerSpec(
        key="aya-101",
        label="Aya 101",
        backend="hf",
        ref="CohereForAI/aya-101",
        family="Cohere",
        vocab_note="250k, mT5 lineage, built for 101 languages",
    ),
    TokenizerSpec(
        key="qwen2.5",
        label="Qwen2.5",
        backend="hf",
        ref="Qwen/Qwen2.5-1.5B-Instruct",
        family="Alibaba",
        vocab_note="152k BPE",
    ),
    TokenizerSpec(
        key="phi4",
        label="Phi-4",
        backend="hf",
        ref="microsoft/phi-4",
        family="Microsoft",
        vocab_note="100k BPE",
    ),
    TokenizerSpec(
        key="deepseek-v3",
        label="DeepSeek V3",
        backend="hf",
        ref="deepseek-ai/DeepSeek-V3",
        family="DeepSeek",
        vocab_note="129k BPE",
    ),
    TokenizerSpec(
        key="aya-expanse",
        label="Aya Expanse",
        backend="hf",
        ref="CohereLabs/aya-expanse-8b",
        family="Cohere",
        # Aya 101 targeted 101 languages; Expanse targets 23. Languages outside
        # that list have no vocabulary coverage at all and fall back to bytes.
        vocab_note="255k, scoped to 23 languages (Aya 101's successor)",
        gated=True,
    ),
    TokenizerSpec(
        key="command-a",
        label="Command A",
        backend="hf",
        ref="CohereLabs/c4ai-command-a-03-2025",
        family="Cohere",
        vocab_note="255k, shares the Aya Expanse vocabulary",
        gated=True,
    ),
    TokenizerSpec(
        key="mistral-small3",
        label="Mistral Small 3",
        backend="hf",
        ref="mistralai/Mistral-Small-24B-Instruct-2501",
        family="Mistral",
        # Shares 131,066 of 131,072 entries with Mistral Nemo yet segments some
        # scripts very differently: the merge table changed, not the vocabulary.
        vocab_note="131k Tekken, near-identical vocab to Nemo but different merges",
    ),
    TokenizerSpec(
        key="gemma3",
        label="Gemma 3",
        backend="hf",
        ref="unsloth/gemma-3-1b-pt",
        family="Google",
        vocab_note="262k SentencePiece; mirror, verified identical to google/gemma-3-1b-pt",
    ),
    TokenizerSpec(
        key="llama4",
        label="Llama 4 Scout",
        backend="hf",
        ref="unsloth/Llama-4-Scout-17B-16E-Instruct",
        family="Meta",
        vocab_note="201k BPE; mirror, verified identical to Meta's Llama-4-Scout",
    ),
    TokenizerSpec(
        key="qwen3",
        label="Qwen3",
        backend="hf",
        ref="Qwen/Qwen3-1.7B",
        family="Alibaba",
        vocab_note="152k BPE",
    ),
    TokenizerSpec(
        key="glm4.5",
        label="GLM-4.5",
        backend="hf",
        ref="zai-org/GLM-4.5-Air",
        family="Zhipu",
        vocab_note="151k BPE",
    ),
    TokenizerSpec(
        key="gpt-oss",
        label="GPT-OSS",
        backend="hf",
        ref="openai/gpt-oss-20b",
        family="OpenAI",
        vocab_note="200k, o200k lineage with open weights",
    ),
    TokenizerSpec(
        key="sea-lion-v3",
        label="Llama-SEA-LION v3",
        backend="hf",
        ref="aisingapore/Llama-SEA-LION-v3-8B-IT",
        family="AI Singapore",
        # Measured, not assumed: the content vocabulary is byte-for-byte Llama
        # 3's. The only differences are three special tokens, so every tax
        # figure here matches Llama 3 exactly.
        vocab_note="Llama 3 vocabulary, unchanged except for 3 special tokens",
    ),
    TokenizerSpec(
        key="phobert",
        label="PhoBERT v2 (Vietnamese-only)",
        backend="hf",
        ref="vinai/phobert-base-v2",
        family="VinAI",
        vocab_note="64k, monolingual Vietnamese baseline",
        languages=("vi",),
    ),
)

BY_KEY: dict[str, TokenizerSpec] = {spec.key: spec for spec in REGISTRY}


def supports(spec: TokenizerSpec, language_code: str) -> bool:
    """Whether measuring ``spec`` against ``language_code`` is meaningful."""
    return spec.languages is None or language_code in spec.languages


def resolve(keys: Iterable[str] | None) -> list[TokenizerSpec]:
    """Map CLI keys to specs. ``None`` or ``["all"]`` selects the ungated set."""
    if keys is None:
        return [s for s in REGISTRY if not s.gated]
    wanted = list(keys)
    if wanted == ["all"]:
        return [s for s in REGISTRY if not s.gated]
    if wanted == ["all+gated"]:
        return list(REGISTRY)
    unknown = [k for k in wanted if k not in BY_KEY]
    if unknown:
        raise KeyError(f"unknown tokenizer keys: {', '.join(unknown)}")
    return [BY_KEY[k] for k in wanted]
