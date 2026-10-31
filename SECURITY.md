# Security Policy

## Supported versions

qualreas is a small, single-maintainer research library. Security fixes are made only to the latest release (currently 0.5.x) and to the `master` branch.

## Reporting a vulnerability

Please **do not** report security problems in a public issue, discussion, or pull request.

Instead, use GitHub's private vulnerability reporting: go to the [Security tab](https://github.com/alreich/qualreas/security) of this repository and choose **Report a vulnerability**. Please include:

- a description of the problem and its potential impact,
- the qualreas version and Python version you are using, and
- the smallest example you can give that reproduces it (for instance, the algebra or network file, or Python dictionary, involved).

This is a volunteer project, so response times may vary, but reports will be read and acknowledged as soon as possible. If the problem is confirmed, a fix will be released and, if you wish, you will be credited in the release notes.

## Scope

qualreas reads algebra and network definitions from JSON files and Python dictionaries. Reports about how the library handles malformed or untrusted input of that kind are in scope. Problems in other software (Python itself, networkx, numpy, bitsets, Jupyter) should be reported to those projects.
