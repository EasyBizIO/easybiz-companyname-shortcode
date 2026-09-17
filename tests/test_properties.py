"""Invariant/property tests (ENG-1192 acceptance criteria)."""

import re

import pytest
from fixtures import TICKET_EXAMPLES

from easybiz_companyname_shortcode import pack

CODE_RE = re.compile(r"^[A-Z0-9]{0,10}$")

SAMPLE_NAMES = [name for name, _ in TICKET_EXAMPLES] + [
    "😀🎉",  # no representable [A-Z0-9] content at all -> empty base, not a crash
    "123 Trading",
    "a",
    "",
]


@pytest.mark.parametrize("name", SAMPLE_NAMES)
def test_output_matches_invariant(name):
    assert CODE_RE.match(pack(name))


@pytest.mark.parametrize("name", SAMPLE_NAMES)
def test_deterministic(name):
    assert pack(name) == pack(name)


@pytest.mark.parametrize("code", [expected for _, expected in TICKET_EXAMPLES])
def test_idempotent_on_already_packed_codes(code):
    """Packing an already-packed code (a single ASCII token within budget)
    returns it unchanged — the per-dictionary rollback guarantees this even
    when the code happens to collide with a legal-form/stopword token."""
    assert pack(code) == code
