#!/usr/bin/env sh
pandoc --from=markdown --to=rst --output=README.rst README.md
# python3 setup.py sdist upload -r pypitest
python3 setup.py sdist upload -r pypi
