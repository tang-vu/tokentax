"""Loading a tokenizer and reducing it to a token counter.

Two backends are supported:
  - ``tiktoken``: OpenAI's BPE encodings, addressed by encoding name.
  - ``hf``: any tokenizer.json hosted on the Hugging Face Hub.

Entries marked ``gated`` in the catalog need Hugging Face credentials in
``HF_TOKEN`` plus accepted terms on the Hub, so they are left out of
``--tokenizers all`` and the report records them as skipped. That keeps the
default run reproducible by anyone while still allowing the full comparison for
those with access.

The catalog itself — every tokenizer entry, and selection — is in
:mod:`tokenizer_catalog`, re-exported here so callers have one import.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable

from .tokenizer_catalog import (
    BY_KEY,
    REGISTRY,
    TokenizerSpec,
    resolve,
    supports,
)

__all__ = [
    "BY_KEY", "REGISTRY", "Encoding", "EncodeFn", "TokenizerLoadError",
    "TokenizerSpec", "UNKNOWN_MARKERS", "load", "resolve", "supports",
]

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


# A tokenizer is reduced to this single operation for benchmarking purposes.
EncodeFn = Callable[[str], Encoding]


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
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer
    except ImportError as exc:  # pragma: no cover - dependency is declared
        raise TokenizerLoadError(f"{spec.key}: tokenizers not installed") from exc

    # Downloading the file explicitly rather than using Tokenizer.from_pretrained,
    # which ignores HF_TOKEN and so fails on gated repos even with valid
    # credentials in the environment.
    try:
        path = hf_hub_download(
            spec.ref, "tokenizer.json", token=os.environ.get("HF_TOKEN") or None
        )
        tokenizer = Tokenizer.from_file(path)
    except Exception as exc:
        hint = (
            " (gated repo: set HF_TOKEN and accept the model's terms on the Hub)"
            if spec.gated
            else ""
        )
        raise TokenizerLoadError(
            f"{spec.key}: {type(exc).__name__}: {str(exc)[:120]}{hint}"
        ) from exc

    def encode(text: str) -> Encoding:
        result = tokenizer.encode(text, add_special_tokens=False)
        unknown = sum(1 for token in result.tokens if token in UNKNOWN_MARKERS)
        return Encoding(tokens=len(result.ids), unknown=unknown)

    return encode
