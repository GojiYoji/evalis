#!/usr/bin/env python
from dataclasses import dataclass
from io import TextIOWrapper
import sys
import re
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from py_utils.py_loader import load_type_from_path

ROOT_DIR = Path(__file__).parent.parent
GRAMMAR_PATH = ROOT_DIR / "grammar" / "Fablex.g4"


class LineWriter:
    def __init__(self, f: TextIOWrapper):
        self._f = f

    def write(self, line: str):
        self._f.write(f"{line}\n")


@dataclass(frozen=True)
class GrammarInfo:
    reserved_words: list[str]
    binary_ops: list[tuple[str, str]]
    unary_ops: list[tuple[str, str]]


def read_grammar_info() -> GrammarInfo:
    reserved_words: list[str] = []
    binary_ops: list[tuple[str, str]] = []
    unary_ops: list[tuple[str, str]] = []

    with GRAMMAR_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"//\s*(\w+):\s*(.*)", line)
            if m:
                label = m.group(1)
                captured = m.group(2)

                match label:
                    case "RESERVED_WORDS":
                        reserved_words = [w.strip() for w in captured.split(",")]
                    case "BINARY_OPS":
                        binary_ops = [
                            (parts[0], parts[1])
                            for w in captured.split(",")
                            for parts in [list(filter(None, w.strip().split(" ")))]
                        ]
                    case "UNARY_OPS":
                        unary_ops = [
                            (parts[0], parts[1])
                            for w in captured.split(",")
                            for parts in [list(filter(None, w.strip().split(" ")))]
                        ]
                    case "END":
                        break

    return GrammarInfo(
        reserved_words=reserved_words,
        binary_ops=binary_ops,
        unary_ops=unary_ops,
    )


def main(argv):
    if len(argv) < 3:
        print(
            f"[ERROR] Too few arguments. Script must be called with [generate_module] [output_file]"
        )
        exit(1)

    [generate_module_arg, output_arg] = argv[1:]
    generate_module_path = Path(generate_module_arg)
    output_path = Path(output_arg)

    if not generate_module_path.exists() or not generate_module_path.is_file():
        print(f"[ERROR] {generate_module_arg} could not be found or is not a file.")
        exit(1)

    # STEP: Get generate function from module
    generate = load_type_from_path(generate_module_path, "generate")
    grammary_info = read_grammar_info()

    # STEP: Create parent dir if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # STEP: Call generate function writing to output file
    with output_path.open("w", encoding="utf-8") as f:
        writer = LineWriter(f)
        generate(
            writer=writer,
            reserved_keywords=grammary_info.reserved_words,
            binary_ops=grammary_info.binary_ops,
            unary_ops=grammary_info.unary_ops,
        )


if __name__ == "__main__":
    main(sys.argv)
