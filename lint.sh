isort -rc .
autoflake -r --in-place --remove-unused-variables .
black -l 120 .
flake8 --max-line-length 120 .
mypy .
rm -rf .mypy_cache