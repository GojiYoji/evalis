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
import { syntaxError } from './error';

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

export type ParseAstReturn =
  | { ast: EvalisNode; errors: null }
  | { ast: null; errors: SyntaxMessage[] };

/**
 * Parse expression and return result with ast or errors.
 *
 * Does NOT throw - returns a result object that contains either:
 * - ast: The parsed AST node
 * - errors: Array of syntax errors
 *
 * For simple use cases, use evaluateExpression() which throws on errors.
 */
export function parseAst(expression: string): ParseAstReturn {
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

  return { ast, errors: null };
}

export function evaluateAst(
  node: EvalisNode,
  context: unknown,
  options: EvaluatorOptions = {}
): unknown {
  const evaluator = new Evaluator(options);
  return evaluator.evaluate(node, context);
}

/**
 * Evaluate expression and return result.
 *
 * Throws EvalisError if there are syntax errors.
 * For non-throwing parse, use parseAst() directly.
 */
export function evaluateExpression(
  expression: string,
  context: unknown = {},
  options: EvaluatorOptions = {}
): unknown {
  const { ast, errors } = parseAst(expression);

  if (!ast) {
    throw syntaxError(errors);
  }

  return evaluateAst(ast, context, options);
}
