# easybiz-companyname-shortcode

Packs a contragent name in any European language into a short `[A-Z0-9]{0,10}`
code — steps 1-4 of [ENG-1192](https://linear.app/easybiz/issue/ENG-1192).

```sh
pip install easybiz-companyname-shortcode
```

```python
from easybiz_companyname_shortcode import pack, DEFAULT_BUDGET

pack("Société Générale")        # "SOCIETEGEN"
pack("L'Oréal Paris")            # "LOREALPARI"
pack("Société Générale", budget=6)  # shorter budget
```

## What this package does NOT do

- **No uniqueness, no suffixing, no DB access.** This is a pure function: same
  name in, same code out, every time. Uniqueness within a tenant (suffix
  `2..99`, hash fallback, `UNIQUE(company_id, code)`) is each consumer's own
  responsibility against its own database — see ENG-1192 steps 4-5.
- **Empty result is a valid, expected output.** If `pack()` returns `""`, the
  input had no representable `[A-Z0-9]` content after normalisation (e.g. the
  name was entirely emoji or CJK). The caller must apply its own
  scope-specific fallback before uniqueness suffixing (the ticket's suggested
  approach: `sha256(name + tenant_scope_key)`, prefixed with `X`).

## API

```python
def pack(name: str, budget: int = DEFAULT_BUDGET) -> str: ...
```

- `name` — the contragent name, in any European language.
- `budget` — max length of the returned code (default `10`, BOB 50's
  contact-code limit).

## Integrating

1. **Don't** string-truncate a full-budget result to make room for a
   uniqueness suffix — that silently drops information the packer already
   made a deliberate choice about. Instead re-invoke `pack()` with a reduced
   `budget` and append your suffix (ENG-1192 step 4) — see
   `Company._mint_short_name` in `easybiz-master-data-service/mds/models.py`
   for a worked collision-resolution implementation.
2. **Do your own uniqueness/collision handling.** This package is a pure
   function — same name in, same code out.

## Development

```sh
make install   # create venv, install deps
make tests     # run pytest
make linters   # ruff format + check --fix
make build     # build sdist/wheel into dist/
```

## Algorithm

See ENG-1192 for the full spec. Summary of the pipeline (`src/easybiz_companyname_shortcode/packer.py`):

1. Strip apostrophes, run the canonical `easybiz-companyname-normalisation`
   normaliser, glue a *trailing* run of single-letter tokens (`orsted a s` ->
   `orsted as`), ASCII-fold diacritics, uppercase and tokenize.
2. Strip noise: legal-form tokens iteratively from the *end only* (never
   mid-name — `SE Banken` keeps `SE`), stopwords anywhere, common words
   demoted to the end (not removed). Each dictionary rolls back if it would
   empty the token list entirely.
3. Pack into the budget: if it fits, join as-is; otherwise take up to 4
   priority tokens, truncate the head to leave one guaranteed character per
   tail token, and split the remainder across tail tokens (leftmost gets the
   remainder-of-division extra character).

## Releasing

Versions are derived from git tags (`hatch-vcs`) — there's no version string
committed in the repo. To cut a release, run the **Publish Patch / Minor /
Major** workflow (`workflow_dispatch`) from the Actions tab: it lints, tests,
bumps and pushes the next semver tag, then builds and publishes the sdist/wheel
to PyPI using the `PYPI_API_TOKEN` repository secret.
