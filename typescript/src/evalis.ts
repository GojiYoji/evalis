import {
  CharStream,
  CommonTokenStream,
  ErrorListener,
  Recognizer,
} from 'antlr4';
import EvalisLexer from './__gen__/EvalisLexer';
import EvalisParser from './__gen__/EvalisParser';
import { AstBuilder } from './ast';
import { Evaluator } from './eval';
import { EvalisNode, EvaluatorOptions, SyntaxMessage } from './types';

class SyntaxErrorCollector implements ErrorListener<unknown> {
  errors: SyntaxMessage[] = [];

  syntaxError(
    recognizer: Recognizer<unknown>,
    offendingSymbol: unknown,
    line: number,
    column: number,
    msg: string
  ): void {
    this.errors.push({ line, column, message: msg });
  }
}

export function parseAst(expression: string): {
  ast: EvalisNode | null;
  errors: SyntaxMessage[];
} {
  const errorCollector = new SyntaxErrorCollector();

  const inputStream = new CharStream(expression);
  const lexer = new EvalisLexer(inputStream);
  lexer.removeErrorListeners();
  lexer.addErrorListener(errorCollector);

  const tokenStream = new CommonTokenStream(lexer);
  const parser = new EvalisParser(tokenStream);
  parser.removeErrorListeners();
  parser.addErrorListener(errorCollector);

  const tree = parser.parse();

  if (errorCollector.errors.length > 0) {
    return { ast: null, errors: errorCollector.errors };
  }

  const builder = new AstBuilder();
  const ast = builder.visit(tree);

  return { ast, errors: [] };
}

export function evaluateAst(
  node: EvalisNode,
  context: unknown,
  options: EvaluatorOptions = {}
): unknown {
  const evaluator = new Evaluator(options);
  return evaluator.evaluate(node, context);
}

export function evaluateExpression(
  expression: string,
  context: unknown = {},
  options: EvaluatorOptions = {}
): unknown {
  const { ast, errors } = parseAst(expression);

  if (errors.length > 0) {
    throw new Error(`Syntax errors: ${JSON.stringify(errors)}`);
  }

  if (!ast) {
    throw new Error('Failed to parse expression');
  }

  return evaluateAst(ast, context, options);
}
