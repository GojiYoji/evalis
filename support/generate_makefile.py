#!/usr/bin/env python
from io import TextIOWrapper
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
OUT_PATH = ROOT_DIR / "Makefile.gen"

# These are the targets every subdir is expected to provide
COMMON_TARGETS = [
    "build",
    "clean",
    "lint",
    "setup",
    "teardown",
    "test",
    "check_version",
]


def _is_subdir(d: Path):
    makefile_path = d / "Makefile"

    return makefile_path.exists() and makefile_path.is_file()


class LineWriter:
    def __init__(self, f: TextIOWrapper):
        self._f = f

    def write(self, line: str):
        self._f.write(f"{line}\n")


def main():
    subdirs = [d.name for d in ROOT_DIR.iterdir() if _is_subdir(d)]

    with OUT_PATH.open("w", encoding="utf-8") as f:
        writer = LineWriter(f)

        writer.write("# DO NOT EDIT!")
        writer.write("# This Makefile is generated from support/generate_makefile.py")
        writer.write(f"# Subdirs found: {subdirs}")
        writer.write("")
        writer.write("# region: top level ----------------------------------------")
        writer.write(f".PHONY: all {" ".join(COMMON_TARGETS)}")
        writer.write("")
        writer.write("all: build")
        writer.write("")
        for target in COMMON_TARGETS:
            writer.write(f"{target}: {" ".join(f"{target}_{x}" for x in subdirs)}")
            writer.write("")

        for subdir in subdirs:
            writer.write(f"# region: {subdir} ----------------------------------------")
            writer.write(
                f".PHONY: {" ".join(f"{target}_{subdir}" for target in COMMON_TARGETS)}"
            )
            writer.write("")
            for target in COMMON_TARGETS:
                writer.write(f"{target}_{subdir}:")
                writer.write(f"\t$(MAKE) -C {subdir} {target}")
                writer.write("")


if __name__ == "__main__":
    main()
