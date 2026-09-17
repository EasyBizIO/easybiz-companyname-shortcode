"""Shortcode packer (ENG-1192, steps 1-3): name -> [A-Z0-9]{0,budget} base code.

Deliberately stops short of step 4 (uniqueness/suffixing) and step 5 (DB writes) —
those need a per-tenant scope key and a database, which vary per consumer. A result
of "" means the input had no representable [A-Z0-9] content after folding (e.g. the
name was entirely emoji/CJK); the caller is responsible for its own scope-specific
fallback in that case.
"""

import re

from easybiz_companyname_normalisation import normalise_name

from .diacritics import fold_diacritics
from .dictionaries import COMMON_WORDS, LEGAL_FORMS, STOPWORDS

DEFAULT_BUDGET = 10

_APOSTROPHES_RE = re.compile("['’‘´]")
_TRAILING_SINGLE_LETTER_RUN_RE = re.compile(r"(?:\b[a-z]\s+)+\b[a-z]$")
_NON_ALNUM_RE = re.compile(r"[^A-Z0-9]+")


def pack(name: str, budget: int = DEFAULT_BUDGET) -> str:
    tokens = _tokenize(name)
    tokens = _remove_noise(tokens)
    return _pack_tokens(tokens, budget)


def _tokenize(raw: str) -> list[str]:
    without_apostrophes = _APOSTROPHES_RE.sub("", raw)
    canonical = normalise_name(without_apostrophes)
    glued = _glue_trailing_single_letters(canonical)
    folded = fold_diacritics(glued)
    return [t for t in _NON_ALNUM_RE.split(folded.upper()) if t]


def _glue_trailing_single_letters(text: str) -> str:
    match = _TRAILING_SINGLE_LETTER_RUN_RE.search(text)
    if not match:
        return text
    glued = match.group(0).replace(" ", "")
    return text[: match.start()] + glued


def _remove_noise(tokens: list[str]) -> list[str]:
    tokens = _strip_trailing_legal_forms(tokens)
    tokens = _strip_stopwords(tokens)
    return _demote_common_words(tokens)


def _strip_trailing_legal_forms(tokens: list[str]) -> list[str]:
    if not tokens:
        return tokens
    stripped = list(tokens)
    while stripped and stripped[-1] in LEGAL_FORMS:
        stripped.pop()
    return stripped or tokens


def _strip_stopwords(tokens: list[str]) -> list[str]:
    if not tokens:
        return tokens
    stripped = [t for t in tokens if t not in STOPWORDS]
    return stripped or tokens


def _demote_common_words(tokens: list[str]) -> list[str]:
    meaningful = [t for t in tokens if t not in COMMON_WORDS]
    common = [t for t in tokens if t in COMMON_WORDS]
    return meaningful + common


def _pack_tokens(tokens: list[str], budget: int) -> str:
    if not tokens:
        return ""
    joined = "".join(tokens)
    if len(joined) <= budget:
        return joined

    k = min(len(tokens), 4)
    head, *tail = tokens[:k]
    head_part = head[: budget - (k - 1)]
    if not tail:
        return head_part

    remaining = budget - len(head_part)
    base, extra = divmod(remaining, len(tail))
    parts = [head_part]
    for i, token in enumerate(tail):
        share = base + (1 if i < extra else 0)
        parts.append(token[:share])
    return "".join(parts)
