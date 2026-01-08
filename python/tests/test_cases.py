import pytest
import yaml
from pathlib import Path
from evalis.evalis import evaluate_expression
from evalis.types import EvaluatorOptions

DIR_BASE = Path(__file__).resolve().parent.parent.parent
TEST_ORACLE_YML = DIR_BASE / "test-oracle" / "cases.yml"

with TEST_ORACLE_YML.open("r", encoding="utf-8") as f:
    TEST_CASES = yaml.safe_load(f)


@pytest.mark.parametrize("test_case", TEST_CASES)
def test_evaluate_expression(test_case):
    expr = test_case["expr"]
    context = test_case.get("context", {})
    expected = test_case["expected"]
    should_null_on_bad_access = test_case.get("should_null_on_bad_access", False)

    result = evaluate_expression(
        expr,
        context,
        EvaluatorOptions(should_null_on_bad_access=should_null_on_bad_access),
    )

    assert (
        result == expected
    ), f"Failed expr: {expr} with context: {context}, got {result}"
