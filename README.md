# sqlnaut

## Installation

First, **ensure that you have FUSE installed**.
Second:

```sh
poetry install
```

## Usage

For FUSE usage:

```sh
python sqlnaut/fs.py <path_to_sqlite.db>
```

Without FUSE (no posix goodies):

```sh
python sqlnaut/utils.py <path_to_sqlite.db>
```

## Things I Might Get Around To

- [ ] documenting the FUSE installation process
- [ ] improving the README
- [ ] removing the non-FUSE option
- [ ] making it pip-installable
- [ ] creating a single, installed `sqlnaut` command
