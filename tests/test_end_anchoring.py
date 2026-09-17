"""Regression tests for end-anchored legal-form stripping (ENG-1192).

The bug this guards against: treating a bare legal-form token (e.g. "SA") as
noise wherever it appears, instead of only at the end of the token list. That
swallows real words that happen to collide with a legal-form abbreviation
mid-name (SE Banken, La Se Rena) and, symmetrically, a mid-name single-letter
run must not get glued into a fake trailing legal form either (Foo S A Bar,
U S A Trading).
"""

import pytest

from easybiz_companyname_shortcode import pack

CASES = [
    ("SE Banken", "SEBANKEN"),
    ("La Se Rena", "SERENA"),
    ("Foo S A Bar", "FOOSBAR"),
    ("U S A Trading", "USTRADING"),
]


@pytest.mark.parametrize("name,expected", CASES)
def test_end_anchoring(name, expected):
    assert pack(name) == expected
