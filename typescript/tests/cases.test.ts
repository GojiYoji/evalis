import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { evaluateExpression } from '../src/evalis';

interface TestCase {
  expr: string;
  context?: unknown;
  expected?: unknown;
  expected_error?: string;
  should_null_on_bad_access?: boolean;
}

describe('Evalis Test Cases', () => {
  const testCasesPath = path.join(__dirname, '../../test-oracle/cases.yml');
  const testCasesYaml = fs.readFileSync(testCasesPath, 'utf8');
  const testCases = yaml.load(testCasesYaml) as TestCase[];

  testCases.forEach((testCase) => {
    const {
      expr,
      context = {},
      expected,
      expected_error: expectedError,
      should_null_on_bad_access: shouldNullOnBadAccess,
    } = testCase;

    const act = () =>
      evaluateExpression(expr, context, { shouldNullOnBadAccess });

    if (expectedError) {
      it(`should error: ${expr}`, () => {
        expect(act).toThrow(new RegExp(expectedError));
      });
    } else {
      it(`should evaluate: ${expr}`, () => {
        expect(act()).toEqual(expected);
      });
    }
  });
});
