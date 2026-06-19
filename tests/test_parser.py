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
        ("2 + 3 * 4", 14.0),
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
        
    def test_nofunction_parser(self):
        parser = ExpressionParser(unary_functions={})
        result = parser("3 + 4")
        while isinstance(result, list) and len(result) > 0:
            result = result[0]
        assert result == 7.0, f"Expected 7.0 but got {result} for expression: 3 + 4"

    def test_variable_substitution(self):
        parser = ExpressionParser(variable_names=["x", "y"])
        result = parser("x + y * 2", variables={"x": 1.0, "y": 3.0})
        while isinstance(result, list) and len(result) > 0:
            result = result[0]
        assert result == 7.0, f"Expected 7.0 but got {result}"

    def test_variable_missing_value_raises(self):
        parser = ExpressionParser(variable_names=["x"])
        with pytest.raises(ValueError, match="x"):
            parser("x")

    def test_variable_value_is_reset_between_calls(self):
        parser = ExpressionParser(variable_names=["x"])
        first = parser("x", variables={"x": 5.0})
        while isinstance(first, list) and len(first) > 0:
            first = first[0]
        assert first == 5.0
        with pytest.raises(ValueError, match="x"):
            parser("x")

    def test_custom_constant(self):
        parser = ExpressionParser(constants={"tau": 6.283185307179586})
        result = parser("tau")
        while isinstance(result, list) and len(result) > 0:
            result = result[0]
        assert result == 6.283185307179586

    def test_overlapping_constant_and_variable_names_raises(self):
        with pytest.raises(ValueError, match="x"):
            ExpressionParser(variable_names=["x"], constants={"x": 1.0})

    def test_imaginary_unit_name_as_variable_raises(self):
        with pytest.raises(ValueError, match="imaginary"):
            ExpressionParser(variable_names=["i"])