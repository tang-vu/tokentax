"""Registry of tokenizers under test, plus uniform loading.

Two backends are supported:
  - ``tiktoken``: OpenAI's BPE encodings, addressed by encoding name.
  - ``hf``: any tokenizer.json hosted on the Hugging Face Hub.

Some Hub repos are gated (Llama, Gemma). They stay in the registry so the
comparison is honest about what was skipped, but loading them requires the
caller to be authenticated; failures surface as ``TokenizerLoadError``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable

# Token strings that mean "this tokenizer cannot represent the input".
# Their presence makes a token count meaningless: text is being destroyed, not
# merely encoded expensively, and the resulting ratio tends to look flattering.
UNKNOWN_MARKERS = frozenset({"<unk>", "[UNK]", "<|unk|>", "<UNK>", "�"})


class TokenizerLoadError(RuntimeError):
    """Raised when a tokenizer cannot be fetched or constructed."""


@dataclass(frozen=True)
class Encoding:
    """Token count for one string, plus how much of it was unrepresentable."""

    tokens: int
    unknown: int = 0


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
        vocab_note="128k BPE; community mirror, Meta's own repo is gated",
    ),
    TokenizerSpec(
        key="gemma2",
        label="Gemma 2",
        backend="hf",
        ref="unsloth/gemma-2-2b",
        family="Google",
        vocab_note="256k SentencePiece; community mirror, Google's repo is gated",
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
        key="deepseek-v3",
        label="DeepSeek V3",
        backend="hf",
        ref="deepseek-ai/DeepSeek-V3",
        family="DeepSeek",
        vocab_note="129k BPE",
    ),
    TokenizerSpec(
        key="gemma3",
        label="Gemma 3",
        backend="hf",
        ref="unsloth/gemma-3-1b-pt",
        family="Google",
        vocab_note="262k SentencePiece; community mirror",
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

# A tokenizer is reduced to this single operation for benchmarking purposes.
EncodeFn = Callable[[str], Encoding]


def supports(spec: TokenizerSpec, language_code: str) -> bool:
    """Whether measuring ``spec`` against ``language_code`` is meaningful."""
    return spec.languages is None or language_code in spec.languages


def load(spec: TokenizerSpec) -> EncodeFn:
    """Return a callable mapping text -> :class:`Encoding` for ``spec``.

    Special tokens are excluded everywhere: we measure the cost of the content
    itself, not of a particular chat template.
    """
    if spec.backend == "tiktoken":
        return _load_tiktoken(spec)
    if spec.backend == "hf":
        return _load_hf(spec)
    raise TokenizerLoadError(f"{spec.key}: unknown backend {spec.backend!r}")


def _load_tiktoken(spec: TokenizerSpec) -> EncodeFn:
    try:
        import tiktoken
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise TokenizerLoadError(f"{spec.key}: tiktoken not installed") from exc
    try:
        encoding = tiktoken.get_encoding(spec.ref)
    except Exception as exc:
        raise TokenizerLoadError(f"{spec.key}: {type(exc).__name__}: {exc}") from exc

    # tiktoken encodings are byte-level BPE: every byte sequence is
    # representable, so there is no unknown-token failure mode.
    return lambda text: Encoding(tokens=len(encoding.encode(text)), unknown=0)


def _load_hf(spec: TokenizerSpec) -> EncodeFn:
    try:
        from tokenizers import Tokenizer
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise TokenizerLoadError(f"{spec.key}: tokenizers not installed") from exc
    try:
        tokenizer = Tokenizer.from_pretrained(spec.ref)
    except Exception as exc:
        hint = " (gated repo: run `huggingface-cli login`)" if spec.gated else ""
        raise TokenizerLoadError(
            f"{spec.key}: {type(exc).__name__}: {str(exc)[:120]}{hint}"
        ) from exc

    def encode(text: str) -> Encoding:
        result = tokenizer.encode(text, add_special_tokens=False)
        unknown = sum(1 for token in result.tokens if token in UNKNOWN_MARKERS)
        return Encoding(tokens=len(result.ids), unknown=unknown)

    return encode


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
