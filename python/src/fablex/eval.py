from typing import Any
from fablex.ast import (
    BinaryOpType,
    LiteralNode,
    BinaryOpNode,
    ReferenceNode,
    UnaryOpNode,
    UnaryOpType,
)


def get_val_from_context(context: Any, key: Any) -> Any:
    if isinstance(context, dict):
        return context[key]
    elif isinstance(context, list):
        return context[key]
    else:
        raise ValueError(f"Unexpected context type in get_val_from_context: {context}")


class FablexEval:
    _should_null_on_bad_access: bool

    def __init__(self, should_null_on_bad_access: bool = False):
        self._should_null_on_bad_access = should_null_on_bad_access

    def evaluate(self, node: Any, context: Any) -> Any:
        if isinstance(node, LiteralNode):
            return node.value
        if isinstance(node, BinaryOpNode):
            left = self.evaluate(node.left, context)
            right = self.evaluate(node.right, context)

            match (node.op):
                case BinaryOpType.ADD:
                    return left + right
                case BinaryOpType.AND:
                    return left and right
                case BinaryOpType.DIVIDE:
                    return left / right
                case BinaryOpType.NOT_EQUALS:
                    return left != right
                case BinaryOpType.EQUALS:
                    return left == right
                case BinaryOpType.GT:
                    return left > right
                case BinaryOpType.GTE:
                    return left >= right
                case BinaryOpType.LT:
                    return left < right
                case BinaryOpType.LTE:
                    return left <= right
                case BinaryOpType.MULTIPLY:
                    return left * right
                case BinaryOpType.OR:
                    return left or right
                case BinaryOpType.SUBTRACT:
                    return left - right
                case _:
                    raise ValueError(f"Unexpected binary op found: {node.op}")
        if isinstance(node, UnaryOpNode):
            val = self.evaluate(node.expr, context)

            match (node.op):
                case UnaryOpType.NOT:
                    return not val
                case _:
                    raise ValueError(f"Unexpected unary op found: {node.op}")

        if isinstance(node, ReferenceNode):
            current = self._lookup_reference(context, node.root)
            for child in node.children:
                child_key = self.evaluate(child, context)
                current = self._lookup_reference(current, child_key)

            return current

        raise ValueError(f"Unexpected node type found: {node}")

    def _lookup_reference(self, context: Any, key: Any) -> Any:
        try:
            return get_val_from_context(context, key)
        except Exception:
            if self._should_null_on_bad_access:
                return None
            else:
                raise
