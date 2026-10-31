# Contributing to qualreas

Thanks for your interest in **qualreas**, a small Python library for qualitative reasoning with relation algebras (Allen's interval algebra, the Region Connection Calculus, and the point and branching-time extensions from Reich's 1994 paper). Bug reports, questions, documentation fixes, new tests, and code contributions are all welcome.

By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Reporting bugs and suggesting features

Please use the [issue forms](https://github.com/alreich/qualreas/issues/new/choose). For a bug, the most useful thing you can include is a short, self-contained example that reproduces it, plus the output or traceback you got. For anything larger than a small fix (a new algebra, a change to the public API), please open an issue to discuss it before writing the code.

To report a security problem, see [SECURITY.md](SECURITY.md) instead of opening a public issue.

## Setting up for development

qualreas requires Python 3.9 or later. Fork the repository, clone your fork, and install it in editable mode from the top-level directory (the one containing `pyproject.toml`):

```
git clone https://github.com/<your-username>/qualreas.git
cd qualreas
pip install -e .
```

This also installs the dependencies (bitsets, networkx, numpy). After that, `import qualreas as qr` works from any directory, and edits to `src/qualreas.py` take effect immediately.

## Running the tests

```
python -m unittest discover -s tests -v
```

`pytest tests` works too if you have pytest installed. The unit tests are in `tests/test_qualreas.py`. Please add or update tests for any change to the code; new tests for existing behavior are welcome as well.

There is also a quick smoke test:

```
python src/qualreas.py
```

GitHub Actions runs the unit tests on Python 3.9 through 3.14 (Ubuntu) and 3.13 (macOS) for every push and pull request. It also fails on Python `SyntaxWarning`s, which you can check locally with:

```
python -W error::SyntaxWarning -m py_compile src/qualreas.py tests/test_qualreas.py
```

## Notebooks, README, and documentation

- **README.md is generated from `notebooks/README.ipynb`.** To change the README, edit the notebook, re-run it from top to bottom, and then export it from the top-level directory:

  ```
  jupyter nbconvert --to markdown notebooks/README.ipynb --output-dir=. --output README
  ```

  Please don't edit `README.md` directly, because the next export would overwrite the change.
- Notebooks whose names begin with `WIP_` are works in progress and are intentionally not documented in the README.
- The documentation in `docs/` is built with Sphinx and hosted on [Read the Docs](https://qualreas.readthedocs.io). Several of its pages are generated from notebooks in `notebooks/`. If your change touches such a notebook, mention it in your pull request so the page can be regenerated.
- If you change a notebook, please re-run it from top to bottom so the saved outputs match the code.

## Pull requests

1. Create a branch from `master`.
2. Keep the change focused; unrelated cleanups are easier to review as separate pull requests.
3. Match the style of the surrounding code.
4. Make sure the tests pass, and describe what you changed and why in the pull request. If it fixes an issue, link it.

## License

qualreas is released under the [MIT License](LICENSE). By submitting a contribution, you agree that it may be distributed under that license.
