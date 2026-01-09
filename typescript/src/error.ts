import { SyntaxMessage } from './types';

export const CODE_UNKNOWN = 'UNKNOWN';
export const CODE_SYNTAX_ERROR = 'SYNTAX_ERROR';
export const CODE_TYPE_ERROR = 'TYPE_ERROR';

export class EvalisError extends Error {
  public readonly code: string;

  constructor(message: string, code: string = CODE_UNKNOWN) {
    super(message);
    this.name = 'EvalisError';
    this.code = code;
  }

  toString(): string {
    return `[Evalis::${this.code}] ${this.message}`;
  }
}

export function syntaxError(errors: SyntaxMessage[]): EvalisError {
  const syntaxErrorMessages = errors
    .map((x) => `${x.line}:${x.column}: ${x.message}`)
    .join('\n');

  const message = `Syntax errors found while tring to evaluate the expression:\n${syntaxErrorMessages}\n`;

  return new EvalisError(message, CODE_SYNTAX_ERROR);
}
