from dataclasses import dataclass
from typing import Any
from evalis.__gen__.grammar import BinaryOpType, UnaryOpType


# region: ast nodes -----------------------------------------------------------
@dataclass(frozen=True)
class ReferenceNode:
    root: str
    children: "tuple[EvalisNode, ...]"


@dataclass(frozen=True)
class UnaryOpNode:
    op: UnaryOpType
    expr: Any


@dataclass(frozen=True)
class BinaryOpNode:
    op: BinaryOpType
    left: Any
    right: Any


@dataclass(frozen=True)
class LiteralNode:
    value: Any


EvalisNode = ReferenceNode | UnaryOpNode | BinaryOpNode | LiteralNode


# region: other types -------------------------------------------------------
@dataclass(frozen=True)
class EvaluatorOptions:
    should_null_on_bad_access: bool = False


@dataclass(frozen=True)
class SyntaxMessage:
    line: int
    column: int
    message: str
