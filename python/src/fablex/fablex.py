from typing import Any

from fablex.antlr4_adapter import parse_expression_tree
from fablex.ast import FablexAstBuilder, FablexNode
from fablex.eval import FablexEval
from fablex.types import FablexEvalOptions


def parse_ast(expression: str) -> FablexNode:
    tree = parse_expression_tree(expression)

    builder = FablexAstBuilder()
    return builder.visit(tree)


def evaluate_ast(
    node: FablexNode,
    context: dict[str, Any] = {},
    options: FablexEvalOptions = FablexEvalOptions(),
) -> Any:
    evaluator = FablexEval(options)
    result = evaluator.evaluate(node, context)

    return result


def evaluate_expression(
    expression: str,
    context: dict[str, Any] = {},
    options: FablexEvalOptions = FablexEvalOptions(),
) -> Any:
    ast = parse_ast(expression)

    return evaluate_ast(ast, context, options)
