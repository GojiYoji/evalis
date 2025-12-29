#!/usr/bin/env python
from io import TextIOWrapper
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
OUT_PATH = ROOT_DIR / "Makefile.gen"

TARGET_CHECK_VERSION = "check_version"

# These are the targets every subdir is expected to provide
COMMON_TARGETS = [
    "build",
    "clean",
    "lint",
    "setup",
    "teardown",
    "test",
    "get_version",
    "get_expression_version",
    "set_version",
]


def _is_subdir(d: Path):
    makefile_path = d / "Makefile"

    return makefile_path.exists() and makefile_path.is_file()


class LineWriter:
    def __init__(self, f: TextIOWrapper):
        self._f = f

    def write(self, line: str):
        self._f.write(f"{line}\n")


def subdir_target(subdir: str, target: str) -> str:
    return f"{subdir}_{target}"


def deps_for_each_subdir(subdirs: list[str], target: str):
    return " ".join(subdir_target(subdir=x, target=target) for x in subdirs)


def deps_for_each_target(subdir: str, targets: list[str]):
    return " ".join(subdir_target(subdir=subdir, target=target) for target in targets)


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
        for target in COMMON_TARGETS:
            writer.write("")
            writer.write(
                f"{target}: {deps_for_each_subdir(subdirs=subdirs, target=target)}"
            )

        writer.write("")
        writer.write(
            f"{TARGET_CHECK_VERSION}: {deps_for_each_subdir(subdirs=subdirs, target=TARGET_CHECK_VERSION)}"
        )

        for subdir in subdirs:
            targets_common = deps_for_each_target(subdir=subdir, targets=COMMON_TARGETS)
            target_check_version = subdir_target(
                subdir=subdir, target=TARGET_CHECK_VERSION
            )

            writer.write("")
            writer.write(f"# region: {subdir} ----------------------------------------")
            writer.write(f".PHONY: {targets_common} {target_check_version}")
            writer.write("")

            # region: common targets for subdir -------------------------------
            for target in COMMON_TARGETS:
                writer.write(f"{subdir_target(subdir=subdir, target=target)}:")
                writer.write(f"\t$(MAKE) -C {subdir} {target}")
                writer.write("")

            # region: check_version for subdir --------------------------------
            writer.write(f"{target_check_version}:")
            writer.write(f"\t@./support/check_subdir_version.sh {subdir}")


if __name__ == "__main__":
    main()
