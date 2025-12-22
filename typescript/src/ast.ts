import { ParseTreeVisitor } from 'antlr4';
import * as Parser from './__gen__/EvalisParser';
import EvalisVisitor from './__gen__/EvalisVisitor';
import { BinaryOpType, UnaryOpType } from './__gen__/grammar';
import { EvalisNode } from './types';

export class AstBuilder
  extends ParseTreeVisitor<EvalisNode>
  implements EvalisVisitor<EvalisNode>
{
  protected defaultResult(): EvalisNode {
    throw new Error('No default result');
  }

  visitParse(ctx: Parser.ParseContext) {
    return this.visit(ctx.expr());
  }

  visitAndExpr(ctx: Parser.AndExprContext): EvalisNode {
    return {
      type: 'binaryOp',
      op: BinaryOpType.AND,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitMulDivExpr(ctx: Parser.MulDivExprContext): EvalisNode {
    const opText = ctx._op?.text;
    if (!opText) throw new Error('Missing operator');

    return {
      type: 'binaryOp',
      op: opText as BinaryOpType,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitEqualityExpr(ctx: Parser.EqualityExprContext): EvalisNode {
    const opText = ctx._op?.text;
    if (!opText) throw new Error('Missing operator');

    return {
      type: 'binaryOp',
      op: opText as BinaryOpType,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitNotExpr(ctx: Parser.NotExprContext): EvalisNode {
    return {
      type: 'unaryOp',
      op: UnaryOpType.NOT,
      expr: this.visit(ctx.expr()),
    };
  }

  visitRelationalExpr(ctx: Parser.RelationalExprContext): EvalisNode {
    const opText = ctx._op?.text;
    if (!opText) throw new Error('Missing operator');

    return {
      type: 'binaryOp',
      op: opText as BinaryOpType,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitAtomExpr(ctx: Parser.AtomExprContext): EvalisNode {
    return this.visit(ctx.atom());
  }

  visitLiteralAtom(ctx: Parser.LiteralAtomContext): EvalisNode {
    return this.visit(ctx.literal());
  }

  visitParenAtom(ctx: Parser.ParenAtomContext): EvalisNode {
    return this.visit(ctx.expr());
  }

  visitIdentifierAtom(ctx: Parser.IdentifierAtomContext): EvalisNode {
    const baseIdentifier = ctx.identifier().getText();
    const parts: EvalisNode[] = [];

    for (const suffix of ctx.accessSuffix_list()) {
      if (suffix.identifier()) {
        parts.push({
          type: 'literal',
          value: suffix.identifier()!.getText(),
        });
      } else if (suffix.expr()) {
        parts.push(this.visit(suffix.expr()!));
      }
    }

    return {
      type: 'reference',
      root: baseIdentifier,
      children: parts,
    };
  }

  visitListComprehension(ctx: Parser.ListComprehensionContext): EvalisNode {
    return {
      type: 'listComprehension',
      elementExpr: this.visit(ctx.expr(0)),
      variableName: ctx.identifier().getText(),
      iterableExpr: this.visit(ctx.expr(1)),
    };
  }

  visitAddSubExpr(ctx: Parser.AddSubExprContext): EvalisNode {
    const opText = ctx._op?.text;
    if (!opText) throw new Error('Missing operator');

    return {
      type: 'binaryOp',
      op: opText as BinaryOpType,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitOrExpr(ctx: Parser.OrExprContext): EvalisNode {
    return {
      type: 'binaryOp',
      op: BinaryOpType.OR,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitInExpr(ctx: Parser.InExprContext): EvalisNode {
    return {
      type: 'binaryOp',
      op: BinaryOpType.IN,
      left: this.visit(ctx.expr(0)),
      right: this.visit(ctx.expr(1)),
    };
  }

  visitNumber(ctx: Parser.NumberContext): EvalisNode {
    const text = ctx.getText();

    if (text.includes('.')) {
      return {
        type: 'literal',
        value: parseFloat(text),
      };
    }

    return {
      type: 'literal',
      value: parseInt(text, 10),
    };
  }

  visitBoolean(ctx: Parser.BooleanContext): EvalisNode {
    return {
      type: 'literal',
      value: ctx.getText() === 'true',
    };
  }

  visitStringLiteral(ctx: Parser.StringLiteralContext): EvalisNode {
    const raw = ctx.getText();
    const unquoted = raw.slice(1, -1);
    const unescaped = unquoted.replace(/\\"/g, '"').replace(/\\\\/g, '\\');

    return {
      type: 'literal',
      value: unescaped,
    };
  }

  visitLiteral(ctx: Parser.LiteralContext): EvalisNode {
    if (ctx.number_()) {
      return this.visit(ctx.number_()!);
    }
    if (ctx.stringLiteral()) {
      return this.visit(ctx.stringLiteral()!);
    }
    if (ctx.boolean_()) {
      return this.visit(ctx.boolean_()!);
    }
    // null
    return {
      type: 'literal',
      value: null,
    };
  }
}
