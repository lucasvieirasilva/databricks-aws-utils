# How to Contribute

## Requirements

- [poetry](https://pypi.org/project/poetry/1.2.0a2/)
  > Please install poetry version `1.2.0a2`
- [mkdocs](https://pypi.org/project/mkdocs/1.2.3/)

## Contributing Code

A good pull request:

- Is clear.
- Complies with the existing codebase style
  ([pre-commit](https://pre-commit.com/))
- Includes [docstrings](https://www.python.org/dev/peps/pep-0257/) and comments
  for unintuitive sections of code.
- Includes documentation for new features.

## Get Started

### Install dependencies

```shell
poetry install -vv
```

After the dependencies being installed, run the command above to activate the virtualenv in your terminal

```shell
poetry shell
```

## Linting

As a pre-deployment step we syntatically validate files with
[pre-commit](https://pre-commit.com).

Please [install pre-commit](https://pre-commit.com/#install) then run
`pre-commit install` to setup the git hooks. Once configured the pre-commit
linters will automatically run on every git commit. Alternatively you
can manually execute the validations by running `pre-commit run --all-files`.
