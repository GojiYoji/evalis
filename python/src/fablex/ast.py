from fablex.__gen__.FablexVisitor import FablexVisitor as BaseFablexVisitor
from fablex.__gen__.FablexParser import FablexParser
from .types import (
    BinaryOpNode,
    BinaryOpType,
    UnaryOpNode,
    UnaryOpType,
    LiteralNode,
    ReferenceNode,
    FablexNode,
)


def _get_op_text(ctx):
    """
    Helper to return ctx.op.text, because this wasn't passing the type checker
    """
    return ctx.op.text


class FablexAstBuilder(BaseFablexVisitor):
    def visitParse(self, ctx):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by FablexParser#AndExpr.
    def visitAndExpr(self, ctx):
        return BinaryOpNode(
            op=BinaryOpType.AND,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by FablexParser#MulDivExpr.
    def visitMulDivExpr(self, ctx: FablexParser.MulDivExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by FablexParser#EqualityExpr.
    def visitEqualityExpr(self, ctx: FablexParser.EqualityExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by FablexParser#NotExpr.
    def visitNotExpr(self, ctx: FablexParser.NotExprContext):
        return UnaryOpNode(op=UnaryOpType.NOT, expr=self.visit(ctx.expr()))

    # Visit a parse tree produced by FablexParser#RelationalExpr.
    def visitRelationalExpr(self, ctx: FablexParser.RelationalExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    def visitAtomExpr(self, ctx: FablexParser.AtomExprContext):
        # LiteralNode
        if ctx.atom().literal():
            return self.visit(ctx.atom().literal())

        # Parentheses
        if ctx.atom().expr():
            return self.visit(ctx.atom().expr())

        # Identifier (+ optional access suffixes)
        base_identifier = ctx.atom().identifier().getText()
        parts: list[FablexNode] = []

        for suffix in ctx.atom().accessSuffix():
            # Dot access
            if suffix.identifier():
                parts.append(LiteralNode(suffix.identifier().getText()))
            # Index access (e.g., ["key"])
            elif suffix.expr():
                parts.append(self.visit(suffix.expr()))

        return ReferenceNode(root=base_identifier, children=tuple(parts))

    # Visit a parse tree produced by FablexParser#AddSubExpr.
    def visitAddSubExpr(self, ctx: FablexParser.AddSubExprContext):
        return BinaryOpNode(
            op=BinaryOpType(_get_op_text(ctx)),
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by FablexParser#OrExpr.
    def visitOrExpr(self, ctx: FablexParser.OrExprContext):
        return BinaryOpNode(
            op=BinaryOpType.OR,
            left=self.visit(ctx.expr(0)),
            right=self.visit(ctx.expr(1)),
        )

    # Visit a parse tree produced by FablexParser#number.
    def visitNumber(self, ctx: FablexParser.NumberContext):
        text: str = ctx.getText()

        if "." in text:
            return LiteralNode(float(text))

        return LiteralNode(int(text))

    # Visit a parse tree produced by FablexParser#boolean.
    def visitBoolean(self, ctx: FablexParser.BooleanContext):
        return LiteralNode(ctx.getText() == "true")

    # Visit a parse tree produced by FablexParser#identifier.
    # Visit a parse tree produced by FablexParser#stringLiteralNode.
    def visitStringLiteralNode(self, ctx: FablexParser.StringLiteralContext):
        raw = ctx.getText()
        unquoted = raw[1:-1]
        unescaped = unquoted.replace('\\"', '"').replace("\\\\", "\\")
        return LiteralNode(unescaped)
