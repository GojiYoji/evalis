import { BinaryOpType, UnaryOpType } from './__gen__/grammar';
import {
  EvalisNode,
  BinaryOpNode,
  UnaryOpNode,
  ReferenceNode,
  LiteralNode,
  ListComprehensionNode,
  EvaluatorOptions,
} from './types';
import { EvalisError, CODE_TYPE_ERROR } from './error';
import { isNullish, shouldStrConcat, isPrimitive, asString } from './utils';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
function getValFromContext(context: any, key: any): any {
  if (Array.isArray(context)) {
    return context[key];
  }
  if (typeof context === 'object' && context !== null) {
    return context[key];
  }
  throw new Error(`Unexpected context type in getValFromContext: ${context}`);
}

export class Evaluator {
  private options: EvaluatorOptions;

  constructor(options: EvaluatorOptions = {}) {
    this.options = options;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  evaluate(node: EvalisNode, context: any): any {
    const nodeType = node.type;

    if (nodeType === 'literal') {
      return (node as LiteralNode).value;
    }

    if (nodeType === 'binaryOp') {
      const binNode = node as BinaryOpNode;
      const left = this.evaluate(binNode.left, context);
      const right = this.evaluate(binNode.right, context);

      switch (binNode.op) {
        case BinaryOpType.ADD:
          // There are only a few types of legal additions:
          // 1. null + null (or undefined)
          // 2. String concatenation
          // 3. Numeric addition
          // 4. List concatenation
          if (isNullish(left) && isNullish(right)) {
            return null;
          } else if (shouldStrConcat(left, right)) {
            return asString(left) + asString(right);
          } else if (isPrimitive(left) && isPrimitive(right)) {
            return left + right;
          } else if (Array.isArray(left) && Array.isArray(right)) {
            return left.concat(right);
          } else {
            throw new EvalisError(
              `Cannot use + operator with types ${typeof left} and ${typeof right}`,
              CODE_TYPE_ERROR
            );
          }
        case BinaryOpType.AND:
          return left && right;
        case BinaryOpType.DIVIDE:
          return left / right;
        case BinaryOpType.NOT_EQUALS:
          return left !== right;
        case BinaryOpType.EQUALS:
          return left === right;
        case BinaryOpType.GT:
          return left > right;
        case BinaryOpType.GTE:
          return left >= right;
        case BinaryOpType.LT:
          return left < right;
        case BinaryOpType.LTE:
          return left <= right;
        case BinaryOpType.MULTIPLY:
          return left * right;
        case BinaryOpType.OR:
          return left || right;
        case BinaryOpType.SUBTRACT:
          return left - right;
        case BinaryOpType.IN:
          return right.includes(left);
        default:
          throw new Error(`Unexpected binary op found: ${binNode.op}`);
      }
    }

    if (nodeType === 'unaryOp') {
      const unNode = node as UnaryOpNode;
      const val = this.evaluate(unNode.expr, context);

      switch (unNode.op) {
        case UnaryOpType.NOT:
          return !val;
        default:
          throw new Error(`Unexpected unary op found: ${unNode.op}`);
      }
    }

    if (nodeType === 'reference') {
      const refNode = node as ReferenceNode;
      let current = this.lookupReference(context, refNode.root);

      for (const child of refNode.children) {
        const childKey = this.evaluate(child, context);
        current = this.lookupReference(current, childKey);
      }

      return current;
    }

    if (nodeType === 'listComprehension') {
      const compNode = node as ListComprehensionNode;
      const iterable = this.evaluate(compNode.iterableExpr, context);

      if (!Array.isArray(iterable)) {
        if (this.options.shouldNullOnBadAccess) {
          return null;
        } else {
          throw new Error(
            `List comprehension requires iterable to be a list, got ${typeof iterable}`
          );
        }
      }

      const results = [];
      for (const item of iterable) {
        const scopedContext = { ...context, [compNode.variableName]: item };
        const result = this.evaluate(compNode.elementExpr, scopedContext);
        results.push(result);
      }

      return results;
    }

    throw new Error(`Unexpected node type found: ${nodeType}`);
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private lookupReference(context: any, key: any): any {
    try {
      return getValFromContext(context, key);
    } catch (err) {
      if (this.options.shouldNullOnBadAccess) {
        return null;
      } else {
        throw err;
      }
    }
  }
}
