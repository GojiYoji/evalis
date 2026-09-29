import { BinaryOpType, UnaryOpType } from './__gen__/grammar';

// region: ast nodes -----------------------------------------------------------
export interface ReferenceNode {
  type: 'reference';
  root: string;
  children: EvalisNode[];
}

export interface UnaryOpNode {
  type: 'unaryOp';
  op: UnaryOpType;
  expr: EvalisNode;
}

export interface BinaryOpNode {
  type: 'binaryOp';
  op: BinaryOpType;
  left: EvalisNode;
  right: EvalisNode;
}

export interface LiteralNode {
  type: 'literal';
  value: unknown;
}

export interface ListComprehensionNode {
  type: 'listComprehension';
  elementExpr: EvalisNode;
  variableName: string;
  iterableExpr: EvalisNode;
}

export interface SliceNode {
  type: 'slice';
  target: EvalisNode;
  lower: EvalisNode | null;
  upper: EvalisNode | null;
}

export interface ListLiteralNode {
  type: 'listLiteral';
  elements: EvalisNode[];
}

export type EvalisNode =
  | ReferenceNode
  | UnaryOpNode
  | BinaryOpNode
  | LiteralNode
  | ListComprehensionNode
  | SliceNode
  | ListLiteralNode;

// region: other types -------------------------------------------------------
export interface EvaluatorOptions {
  shouldNullOnBadAccess?: boolean;
}

export interface SyntaxMessage {
  line: number;
  column: number;
  message: string;
}
