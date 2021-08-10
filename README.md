# configparser-black

A module to parse configuration for black from common python config files such as `setup.cfg`, `tox.ini`, etc

## Install

```bash
pip install configparser-black
```

## Run

```bash
cblack
```
or
```bash
python -m cblack
```

## Configuration

Black supports pyproject.toml and global configuration natively.

This module ignores `setup.cfg` and `tox.ini` black related configurations if there is a `[tool.black]` section in your `pyproject.toml`
This module will pass the configuration to black as command line arguments, meaning that it will override any configuration you have in your global black files in
- Windows `~\.black`
- Linux/MacOS: `$XDG_CONFIG_HOME/black` (`~/.config/black` if the `XDG_CONFIG_HOME` environment variable is not set)

If there is no `pyproject.toml` it will lookup for configuration in
1. `setup.cfg`: as `[tool:black]`
2. `tox.ini`: as `[black]`

with the higher number superseeding lower numbers (i.e `tox.ini` overrides any black configuration found in `setup.cfg`)

### setup.cfg
Example configuration in `setup.cfg`
```ini
[tool:black]
line-length = 100
quiet = true
target-version = py37
include = \.pyi?|somerandomfilename$
extend-exclude = ^/foo.py
```

Running
```bash
cblack --check ./
```

black will run with
```bash
black --quiet --line-length 100 --target-version py37 --include '\.pyi?|somerandomfilename' --check ./
```

### tox.ini
Same configuration in `tox.ini`
```ini
[black]
line-length = 79
target-version = ['py37', 'py38']
; Note single and double quotes at the start/end are stripped
include = "\.pyi?$"
extend-exclude = ^/foo.py
```

Running
```bash
cblack ./
```

Similarly black will run with

black will run with
```bash
black --line-length 79 --target-version py36 --target-version py37 --include '\.pyi?$' --extend-exclude '^/foo.py' ./
```

## Notes

### Quotes
Quotes will be stripped from values from start and end. Also there is no need to escape quotes in the middle of a string.

e.g
```ini
include = "somerandomfile"
```

Will be
```bash
black --include "somerandomfile"
# Equivalently in bash
black --include somerandomfile
```

and not
```bash
black --include "\"somerandomfile\""
```

If you want to include quotes you can wrap in single if you want double or double if you want single
i.e
```ini
include = '"somerandomfile"'
extend-exclude = "'somerandomfile'"
```
will be

```bash
black --include "\"somerandomfile\"" --extend-exclude "'somerandomfile'"
```
