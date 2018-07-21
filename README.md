# Iris

Iris is a developers' tool which helps in maintaining changelog.
It can also calculate current version of developed software.

## How it works

Iris scans your git repository and generates changelog for you.
[Changelog](CHANGELOG.md) of this project is also generated by Iris.
The only thing you have to remember is naming commits [Conventional Commits Standard.](https://conventionalcommits.org/)

## Building from source

Install `pyinstaller`:

```
pip install pyinstaller
```

Go to `src` directory and build Iris:

```
cd src
pyinstaller --onefile iris.py
```

Executable file can be found in `src/dist` directory.

## TODO

1. Add all of commits' types
1. Make possibility to calculate current version without generating changelog (useful for CI/CD)
1. Allow to use scope in commit messages (eg. `feat(lang): added polish language`)