"""Golden examples from the ENG-1192 ticket body (see fixtures.py)."""

import pytest
from fixtures import TICKET_EXAMPLES

from easybiz_companyname_shortcode import pack


@pytest.mark.parametrize("name,expected", TICKET_EXAMPLES)
def test_ticket_example(name, expected):
    assert pack(name) == expected
