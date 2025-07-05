from typing import Protocol


class LineWriter(Protocol):
    def write(self, line: str): ...


def generate(
    writer: LineWriter,
    reserved_keywords: list[str],
    binary_ops: list[tuple[str, str]],
    unary_ops: list[tuple[str, str]],
):
    writer.write("from dataclasses import dataclass")
    writer.write("from enum import Enum")
    writer.write("")
    writer.write("RESERVED_KEYWORDS = [")
    for word in reserved_keywords:
        writer.write(f'    "{word}"')
    writer.write("]")

    writer.write("class BinaryOpType(Enum):")
    for key, value in binary_ops:
        writer.write(f'    {key} = "{value}"')
    writer.write("")

    writer.write("class UnaryOpType(Enum):")
    for key, value in unary_ops:
        writer.write(f'    {key} = "{value}"')
    writer.write("")
