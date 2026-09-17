"""ASCII-folding for the shortcode packer (ENG-1192, step 1.4-1.5).

Operates on lowercase input only — the pipeline always folds after
``normalise_name()`` (which lowercases) and before uppercasing, so uppercase
input is out of scope here rather than defensively handled.

NFKD handles most accented Latin letters (e -> e, u -> u, a -> a, c -> c).
The characters below have no Unicode decomposition mapping at all, so NFKD
leaves them untouched — they need an explicit table.
"""

import unicodedata

_EXPLICIT_FOLDS = {
    "ß": "ss",  # ß
    "ø": "o",  # ø
    "đ": "d",  # đ
    "ð": "d",  # ð
    "þ": "th",  # þ
    "ł": "l",  # ł
    "æ": "ae",  # æ
    "œ": "oe",  # œ
    "ı": "i",  # ı (dotless i)
    "ħ": "h",  # ħ
    "ŋ": "n",  # ŋ
}


def fold_diacritics(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    without_marks = "".join(c for c in decomposed if not unicodedata.combining(c))
    for char, replacement in _EXPLICIT_FOLDS.items():
        without_marks = without_marks.replace(char, replacement)
    return without_marks
