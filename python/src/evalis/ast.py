from evalis.__gen__.EvalisVisitor import EvalisVisitor as BaseEvalisVisitor
from evalis.__gen__.EvalisParser import EvalisParser
from .types import (
    BinaryOpNode,
    BinaryOpType,
    UnaryOpNode,
    UnaryOpType,
    LiteralNode,
    ReferenceNode,
    EvalisNode,
)


def _get_op_text(ctx):
    """
    Helper to return ctx.op.text, because this wasn't passing the type checker
    """
    return ctx.op.text


class AstBuilder(BaseEvalisVisitor):
    def visitParse(self, ctx):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by EvalisParser#AndExpr.
    def visitAndExpr(self, ctx):
        return BinaryOpNode(
            op=BinaryOpType.AND,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by EvalisParser#MulDivExpr.
    def visitMulDivExpr(self, ctx: EvalisParser.MulDivExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by EvalisParser#EqualityExpr.
    def visitEqualityExpr(self, ctx: EvalisParser.EqualityExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by EvalisParser#NotExpr.
    def visitNotExpr(self, ctx: EvalisParser.NotExprContext):
        return UnaryOpNode(op=UnaryOpType.NOT, expr=self.visit(ctx.expr()))

    # Visit a parse tree produced by EvalisParser#RelationalExpr.
    def visitRelationalExpr(self, ctx: EvalisParser.RelationalExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    def visitAtomExpr(self, ctx: EvalisParser.AtomExprContext):
        # LiteralNode
        if ctx.atom().literal():
            return self.visit(ctx.atom().literal())

        # Parentheses
        if ctx.atom().expr():
            return self.visit(ctx.atom().expr())

        # Identifier (+ optional access suffixes)
        base_identifier = ctx.atom().identifier().getText()
        parts: list[EvalisNode] = []

        for suffix in ctx.atom().accessSuffix():
            # Dot access
            if suffix.identifier():
                parts.append(LiteralNode(suffix.identifier().getText()))
            # Index access (e.g., ["key"])
            elif suffix.expr():
                parts.append(self.visit(suffix.expr()))

        return ReferenceNode(root=base_identifier, children=tuple(parts))

    # Visit a parse tree produced by EvalisParser#AddSubExpr.
    def visitAddSubExpr(self, ctx: EvalisParser.AddSubExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by EvalisParser#OrExpr.
    def visitOrExpr(self, ctx: EvalisParser.OrExprContext):
        return BinaryOpNode(
            op=BinaryOpType.OR,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    def visitInExpr(self, ctx: EvalisParser.InExprContext):
        return BinaryOpNode(
            op=BinaryOpType.IN,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by EvalisParser#number.
    def visitNumber(self, ctx: EvalisParser.NumberContext):
        text: str = ctx.getText()

        if "." in text:
            return LiteralNode(float(text))

        return LiteralNode(int(text))

    # Visit a parse tree produced by EvalisParser#boolean.
    def visitBoolean(self, ctx: EvalisParser.BooleanContext):
        return LiteralNode(ctx.getText() == "true")

    # Visit a parse tree produced by EvalisParser#stringLiteralNode.
    def visitStringLiteral(self, ctx: EvalisParser.StringLiteralContext):
        raw = ctx.getText()
        unquoted = raw[1:-1]
        unescaped = unquoted.replace('\\"', '"').replace("\\\\", "\\")
        return LiteralNode(unescaped)
