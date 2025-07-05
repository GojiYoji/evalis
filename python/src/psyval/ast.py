from enum import Enum
from psyval.__gen__.grammar.PsyvalVisitor import PsyvalVisitor as BasePsyvalVisitor
from psyval.__gen__.grammar.PsyvalParser import PsyvalParser
from dataclasses import dataclass
from typing import Any


class BinOpType(Enum):
    ADD = "+"
    AND = "and"
    DIVIDE = "/"
    EQUALS = "=="
    NOT_EQUALS = "!="
    GT = ">"
    GTE = ">="
    LT = "<"
    LTE = "<="
    MULTIPLY = "*"
    OR = "or"
    SUBTRACT = "-"


class UnaryOpType(Enum):
    NOT = "not"


@dataclass(frozen=True)
class Reference:
    root: str
    children: "tuple[PsyvalNode, ...]"


@dataclass(frozen=True)
class UnaryOp:
    op: UnaryOpType
    expr: Any


@dataclass(frozen=True)
class BinOp:
    op: BinOpType
    left: Any
    right: Any


@dataclass(frozen=True)
class Literal:
    value: Any


PsyvalNode = Reference | UnaryOp | BinOp | Literal


def _get_op_text(ctx):
    return ctx.op.text


class PsyvalAstBuilder(BasePsyvalVisitor):
    def visitParse(self, ctx):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by PsyvalParser#AndExpr.
    def visitAndExpr(self, ctx):
        return BinOp(
            op=BinOpType.AND,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by PsyvalParser#MulDivExpr.
    def visitMulDivExpr(self, ctx: PsyvalParser.MulDivExprContext):
        return BinOp(
            op=BinOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by PsyvalParser#EqualityExpr.
    def visitEqualityExpr(self, ctx: PsyvalParser.EqualityExprContext):
        return BinOp(
            op=BinOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by PsyvalParser#NotExpr.
    def visitNotExpr(self, ctx: PsyvalParser.NotExprContext):
        return UnaryOp(op=UnaryOpType.NOT, expr=self.visit(ctx.expr()))

    # Visit a parse tree produced by PsyvalParser#RelationalExpr.
    def visitRelationalExpr(self, ctx: PsyvalParser.RelationalExprContext):
        return BinOp(
            op=BinOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    def visitAtomExpr(self, ctx: PsyvalParser.AtomExprContext):
        # Literal
        if ctx.atom().literal():
            return self.visit(ctx.atom().literal())

        # Parentheses
        if ctx.atom().expr():
            return self.visit(ctx.atom().expr())

        # Identifier (+ optional access suffixes)
        base_identifier = ctx.atom().identifier().getText()
        parts: list[PsyvalNode] = []

        for suffix in ctx.atom().accessSuffix():
            # Dot access
            if suffix.identifier():
                parts.append(Literal(suffix.identifier().getText()))
            # Index access (e.g., ["key"])
            elif suffix.expr():
                parts.append(self.visit(suffix.expr()))

        return Reference(root=base_identifier, children=tuple(parts))

    # Visit a parse tree produced by PsyvalParser#AddSubExpr.
    def visitAddSubExpr(self, ctx: PsyvalParser.AddSubExprContext):
        return BinOp(
            op=BinOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by PsyvalParser#OrExpr.
    def visitOrExpr(self, ctx: PsyvalParser.OrExprContext):
        return BinOp(
            op=BinOpType.OR, left=self.visit(ctx.expr(0)), right=self.visit(ctx.expr(1))
        )

    # Visit a parse tree produced by PsyvalParser#number.
    def visitNumber(self, ctx: PsyvalParser.NumberContext):
        text: str = ctx.getText()

        if "." in text:
            return Literal(float(text))

        return Literal(int(text))

    # Visit a parse tree produced by PsyvalParser#boolean.
    def visitBoolean(self, ctx: PsyvalParser.BooleanContext):
        return Literal(ctx.getText() == "true")

    # Visit a parse tree produced by PsyvalParser#identifier.
    # Visit a parse tree produced by PsyvalParser#stringLiteral.
    def visitStringLiteral(self, ctx: PsyvalParser.StringLiteralContext):
        raw = ctx.getText()
        unquoted = raw[1:-1]
        unescaped = unquoted.replace('\\"', '"').replace("\\\\", "\\")
        return Literal(unescaped)
