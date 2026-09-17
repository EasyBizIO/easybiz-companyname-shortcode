"""Sanity-pins a few known-good outputs of the upstream canonical normaliser.

We depend on `easybiz-companyname-normalisation` as a plain pip dependency rather
than vendoring/porting it (see plan), so there's no fixture-parity test to run here
— that lives in the upstream package's own CI. This is a cheap tripwire: if a
version bump silently changes output for these known inputs, this fails loudly
instead of us finding out via a wrong code in production.
"""

from easybiz_companyname_normalisation import NORMALISER_VERSION, normalise_name

# A handful of rows lifted from upstream's own lu_names.csv fixture.
KNOWN_GOOD = [
    ("ACME S.A.", "acme sa"),
    ("Telindus S.à r.l.", "telindus sarl"),
    ("SE Banken", "se banken"),
    ("La Se Rena", "la se rena"),
    ("Foo S A Bar", "foo s a bar"),
]


def test_pinned_version():
    assert NORMALISER_VERSION == "1.0.0"


def test_known_good_outputs():
    for raw, expected in KNOWN_GOOD:
        assert normalise_name(raw) == expected
