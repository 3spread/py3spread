# Repository Guidelines

Python client for the 3spread API — machine-readable SEC filing data (insider
transactions, 13F holdings, fund portfolios, beneficial ownership, and more).
The package is published to PyPI as `py3spread` and requires Python 3.10+.

## Project Structure & Module Organization

```
src/py3spread/
├── __init__.py        # public exports: Client, exceptions, FAMILIES
├── _version.py        # version string (read by hatchling)
├── client.py          # Client class — auth, request/retry, HTTP transport
├── exceptions.py      # ThreeSpreadError hierarchy + error_from_response mapper
├── py.typed           # PEP 561 marker (typed package)
└── resources/
    ├── _base.py       # Resource base class: _get, _iter_cursor, _iter_offset
    ├── __init__.py    # resource exports + FAMILIES registry
    ├── filings.py, insiders.py, institutional_holdings.py, financials.py, ...
    └── system.py      # Entities, Coverage, Changes, FAMILIES
tests/                 # pytest suite, all via httpx.MockTransport
docs/                  # mkdocs-material site (guides/, reference/)
examples/              # notebooks + assets
.github/workflows/     # CI
```

Each filing family is a `Resource` subclass instantiated on the `Client`.
Pagination is either keyset cursor (`_iter_cursor`) or offset-based
(`_iter_offset`), depending on the endpoint.

## Build, Test, and Development Commands

```bash
uv venv && uv pip install -e ".[dev]"   # create venv, install editable + dev deps
pytest                                  # run the test suite
pytest tests/test_client.py             # run a single test file
pytest -k access_token                  # run tests matching a keyword
uv build                                # build wheel + sdist (used in CI)
mkdocs serve                            # serve docs locally (needs [docs] extra)
```

There is no separate lint or formatter config — match the style of surrounding
code. CI runs `pytest` and `uv build` on Python 3.10–3.13.

## Coding Style & Naming Conventions

- `from __future__ import annotations` at the top of every module.
- 4-space indentation, lines kept under ~90 chars.
- Type annotations on all public signatures; use `|` union syntax (3.10+).
- Class names are `PascalCase`; resource classes match their dataset
  (e.g. `InstitutionalHoldings`, `MoneyMarketFunds`).
- Private helpers are `_prefixed` (`_get`, `_clean_params`, `_iter_cursor`).
- Docstrings are Google-style (per mkdocstrings config); keep them concise
  and focused on caller-facing behavior.
- Use `decimal.Decimal` for monetary values, never `float`.

## Testing Guidelines

Tests use `pytest` with `httpx.MockTransport` — no network calls, no real API
key. The `make_client` fixture (in `conftest.py`) builds a `Client` with a
custom transport handler.

- Test files: `test_client.py`, `test_errors.py`, `test_pagination.py`,
  `test_resources.py`.
- Name tests `test_<behavior>` with snake_case.
- Each test creates a handler function that inspects the request and returns
  a canned `httpx.Response`.
- Run the full suite with `pytest` before pushing.

## Commit & Pull Request Guidelines

- Commit messages are short, lowercase, imperative, no prefix tags:
  `accept an OAuth access token alongside the API key`,
  `give entities/timeseries typed signatures, add offset to changes.list`.
- PRs are merged via GitHub squash/merge — the title becomes the commit
  message. Keep titles descriptive.
- PRs should include relevant tests and pass CI (pytest + build on all
  supported Python versions).
- Branch naming: `feat/<topic>`, `fix/<topic>`, etc.

## Agent-Specific Instructions

- Do not make real API calls in tests. Always use `httpx.MockTransport` via
  the `make_client` fixture.
- When adding a new filing family: create a resource class in
  `src/py3spread/resources/`, register it in `resources/__init__.py`,
  instantiate it on the `Client`, add it to `FAMILIES` in `system.py`,
  and export it from the top-level `__init__.py` `__all__`.
- Keep the public API surface stable; the package is published to PyPI.
- Tickers are uppercased by `_clean_params` before sending — do not uppercase
  them manually in resource methods.
- Monetary and ratio fields are strings at full precision; document this for
  callers but never convert to `float` inside the library.
