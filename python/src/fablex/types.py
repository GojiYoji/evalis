from dataclasses import dataclass
from typing import Any
from fablex.__gen__.grammar import BinaryOpType, UnaryOpType


# region: ast nodes -----------------------------------------------------------
@dataclass(frozen=True)
class ReferenceNode:
    root: str
    children: "tuple[FablexNode, ...]"


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


FablexNode = ReferenceNode | UnaryOpNode | BinaryOpNode | LiteralNode


# region: other types -------------------------------------------------------
@dataclass(frozen=True)
class FablexEvalOptions:
    should_null_on_bad_access: bool = False


@dataclass(frozen=True)
class FablexSyntaxMessage:
    line: int
    column: int
    message: str
