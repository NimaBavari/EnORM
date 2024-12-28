#!/bin/bash
isort -rc .
autoflake -r --in-place --remove-unused-variables .
black -l 120 .
flake8 --max-line-length 120 . --exclude .venv,*/migrations
mypy --disable-error-code import-not-found --explicit-package-bases .
rm -rf .mypy_cache
