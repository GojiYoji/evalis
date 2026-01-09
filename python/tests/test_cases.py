import pytest
import yaml
from pathlib import Path
from evalis.evalis import evaluate_expression
from evalis.types import EvaluatorOptions

DIR_BASE = Path(__file__).resolve().parent.parent.parent
TEST_ORACLE_YML = DIR_BASE / "test-oracle" / "cases.yml"

with TEST_ORACLE_YML.open("r", encoding="utf-8") as f:
    TEST_CASES = yaml.safe_load(f)


def describe_test_case(test_case):
    expr = test_case.get("expr", None)
    desc = test_case.get("description", None)

    if desc:
        return f"test for: {desc}"
    if expr:
        return f"test for expression: {test_case.get("expr")}"

    return ""


@pytest.mark.parametrize("test_case", TEST_CASES, ids=describe_test_case)
def test_evaluate_expression(test_case):
    expr = test_case["expr"]
    context = test_case.get("context", {})
    expected = test_case.get("expected", None)
    expected_error = test_case.get("expected_error", None)
    should_null_on_bad_access = test_case.get("should_null_on_bad_access", False)

    def act():
        return evaluate_expression(
            expr,
            context,
            EvaluatorOptions(should_null_on_bad_access=should_null_on_bad_access),
        )

    if expected_error:
        with pytest.raises(Exception, match=expected_error):
            act()

    else:
        result = act()

        assert (
            result == expected
        ), f"Failed expr: {expr} with context: {context}, got {result}"
