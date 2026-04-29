import pytest
import math
from parsimathious.parser import ExpressionParser, UnaryFunctionMap

class TestExpressionParser:
    
    @pytest.mark.parametrize("expression,expected", [
        ("3", 3.0),
        ("i", 1j),
        ("2i", 2j),
        ("3^2", 9.0),
        ("3*2", 6.0),
        ("10/2", 5.0),
        ("2+2", 4.0),
        ("(3+2)", 5.0),
        ("(1+2)*3", 9.0),
        ("sin(0)", 0.0),
        ("cos(0)", 1.0),
        ("pi", math.pi),
        ("e", math.e),
        ("cos(0)+sin(pi/2)", 2.0),
    ])
    def test_parse_expressions(self, expression: str, expected):
        # Define text unary functions for testing
        unary_functions: UnaryFunctionMap = {
            "sin": math.sin,
        }
        if "cos" in expression:
            # We add it only for cos, so we test both the case
            # of a dictionary with a single function and a dictionary with multiple functions,
            # which can lead to different parsing behavior if not handled correctly
            unary_functions["cos"] = math.cos
        parser = ExpressionParser(unary_functions=unary_functions)
        result = parser(expression)
        # Result may be nested; keep accessing 0 until we get something that is not a list
        while isinstance(result, list) and len(result) > 0:
            result = result[0]
        assert result == expected, f"Expected {expected} but got {result} for expression: {expression}"