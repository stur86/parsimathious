import pytest
from parsimonious.nodes import Node
from parsimathious import ExpressionGrammar

class TestExpressionGrammar:
    
    @pytest.mark.parametrize("expression", [
        "3 + 4",
        "1 + 2i",
        "i",
        "2 * (5 - 1)",
        "10 / 2 + 6",
        "(1 + 2) * (3 + 4)",
        "5 - 3 * 2",
        "sin(0) + cos(0)",
        "log(1) + sqrt(4)",
        "exp(1) + log(100)",
        "abs(-5) + floor(3.7)",
        "ceil(3.2) + round(3.5)",
        "sinh(0) + cosh(0)",
        "tanh(0) + asin(0)",
        "acos(1) + atan(1)",
        "asinh(0) + acosh(1)",
        "atanh(0) + sec(0)",
        "csc(0) + cot(1)"
    ])
    def test_valid_expressions(self, expression: str):
        grammar = ExpressionGrammar()
        parsed = grammar(expression)
        assert parsed is not None, f"Failed to parse: {expression}"
        assert isinstance(parsed, Node), f"Parsed result is not a Node: {expression}"
        assert parsed.expr_name == "expression", f"Top-level node is not 'expression': {expression}"

    @pytest.mark.parametrize("expression", [
        "3 + ",
        "* 5",
        "10 / (2 +",
        "(1 + 2 * (3 + 4)",
        "5 - - 3",
        "2ii"
    ])
    def test_invalid_expressions(self, expression: str):
        grammar = ExpressionGrammar()
        with pytest.raises(Exception, match="Syntax error"):
            grammar(expression)
