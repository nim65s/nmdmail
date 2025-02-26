#!/usr/bin/env python
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "tomlkit",
# ]
# ///

"""Manage version number in pyproject.toml."""

from argparse import ArgumentParser
from pathlib import Path

from tomlkit import dump, load

PYPROJECT = Path("pyproject.toml")

parser = ArgumentParser()
parser.add_argument("cmd", choices=["old", "major", "minor", "patch"])
args = parser.parse_args()

with PYPROJECT.open() as f:
    data = load(f)

old = tuple(int(i) for i in data["project"]["version"].split("."))

match args.cmd:
    case "old":
        new = old
    case "major":
        new = (old[0] + 1, 0, 0)
    case "minor":
        new = (old[0], old[1] + 1, 0)
    case "patch":
        new = (old[0], old[1], old[2] + 1)

version = ".".join(str(i) for i in new)
data["project"]["version"] = version

with PYPROJECT.open("w") as f:
    dump(data, f)

print(version)
