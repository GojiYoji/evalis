#!/usr/bin/env python
import sys
from pathlib import Path

CONSTANTS_PATH = Path(__file__).parent.parent / "src" / "evalis" / "constants.py"


def main(args: list[str]):
    if len(args) < 2 or not args[1]:
        print(f"Usage: python {__file__} <version>")
        print("")
        exit(1)

    version = args[1]

    with CONSTANTS_PATH.open(mode="w") as f:
        f.write(
            f"""# WARNING: This file is auto_generated.
#
# - To change the __version__ in this file, use the `set_version` make target.

# Version of package
__version__ = "{version}"


# Evalis expression version that this package supports
EXPRESSION_VERSION = \"0.1.1\"
"""
        )


if __name__ == "__main__":
    main(sys.argv)
