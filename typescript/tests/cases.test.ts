import * as fs from 'fs';
import * as path from 'path';
import * as yaml from 'js-yaml';
import { evaluateExpression } from '../src/evalis';

interface TestCase {
  expr: string;
  context?: unknown;
  expected: unknown;
  should_null_on_bad_access?: boolean;
}

describe('Evalis Test Cases', () => {
  const testCasesPath = path.join(__dirname, '../../test-oracle/cases.yml');
  const testCasesYaml = fs.readFileSync(testCasesPath, 'utf8');
  const testCases = yaml.load(testCasesYaml) as TestCase[];

  testCases.forEach((testCase) => {
    it(`should evaluate: ${testCase.expr}`, () => {
      const result = evaluateExpression(testCase.expr, testCase.context || {}, {
        shouldNullOnBadAccess: testCase.should_null_on_bad_access || false,
      });

      expect(result).toEqual(testCase.expected);
    });
  });
});
