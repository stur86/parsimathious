import math
from parsimonious import Grammar, ParseError
from parsimonious.nodes import Node
from typing import Dict, Callable, Sequence

UnaryFunction = Callable[[float], float]
UnaryFunctionMap = Dict[str, UnaryFunction]
ConstantMap = Dict[str, float | complex]

_DEFAULT_CONSTANTS: ConstantMap = {
    "pi": math.pi,
    "e": math.e,
}

_DEFAULT_UNARY_FUNCTIONS: UnaryFunctionMap = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "sqrt": math.sqrt,
    "exp": math.exp,
    "log10": math.log10,
    "abs": abs,
    "floor": math.floor,
    "ceil": math.ceil,
    "round": round,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "asinh": math.asinh,
    "acosh": math.acosh,
    "atanh": math.atanh,
    "sec": lambda x: 1 / math.cos(x),
    "csc": lambda x: 1 / math.sin(x),
    "cot": lambda x: 1 / math.tan(x),
}

class ExpressionGrammar:
    _grammar: Grammar
    
    def __init__(
        self,
        unary_functions: UnaryFunctionMap = _DEFAULT_UNARY_FUNCTIONS,
        variable_names: Sequence[str] = (),
        constants: ConstantMap = _DEFAULT_CONSTANTS,
    ):
        overlap = set(constants) & set(variable_names)
        if overlap:
            raise ValueError(f"Names cannot be used as both constants and variables: {', '.join(sorted(overlap))}")
        if "i" in constants or "i" in variable_names:
            raise ValueError('"i" is reserved for the imaginary unit and cannot be used as a constant or variable name')

        grammar_definition = """
            expression = sum / unary_number
            sum = term (add_op term)*
            term = factor (mul_op factor)*
            factor = exp_factor (exp_op exp_factor)*
            exp_factor = atom
            unary_number = unary_op number
            parenthesized_expression = "(" expression ")"
            add_op = "+" / "-"
            mul_op = "*" / "/"
            exp_op = "^"
            unary_op = "+" / "-"
            number = ~r"\\d+(\\.\\d+)?"
            imaginary_unit = "i"
            imaginary_number = number imaginary_unit
        """
        complex_number_alternatives = ["imaginary_number", "number", "imaginary_unit"]
        if len(constants) > 0:
            # Sort them from longest to shortest to ensure correct parsing (e.g., "log10" before "log")
            sorted_constant_names = sorted(constants.keys(), key=len, reverse=True)
            constant_alternatives = " / ".join(f'"{name}"' for name in sorted_constant_names)
            grammar_definition += f"""
            constant = {constant_alternatives}
            """
            complex_number_alternatives.append("constant")
        if len(variable_names) > 0:
            # Sort them from longest to shortest to ensure correct parsing (e.g., "xy" before "x")
            sorted_variable_names = sorted(variable_names, key=len, reverse=True)
            variable_alternatives = " / ".join(f'"{name}"' for name in sorted_variable_names)
            grammar_definition += f"""
            variable = {variable_alternatives}
            """
            complex_number_alternatives.append("variable")
        grammar_definition += f"""
            complex_number = {" / ".join(complex_number_alternatives)}
        """
        if len(unary_functions) > 0:
            function_keys = list(unary_functions.keys())
            # Sort them from longest to shortest to ensure correct parsing (e.g., "log10" before "log")
            function_keys.sort(key=len, reverse=True)
            function_names = " / ".join(f'"{name}"' for name in function_keys)
            grammar_definition += f"""atom = function_call / parenthesized_expression / complex_number
            function_call = function_name parenthesized_expression
            function_name = {function_names}"""
        else:
            grammar_definition += "atom = parenthesized_expression / complex_number"

        self._grammar = Grammar(grammar_definition)

    def __call__(self, expression: str) -> Node:
        # Strip out all spaces
        expression = expression.replace(" ", "")
        try:
            return self._grammar.parse(expression)
        except ParseError as e:
            raise Exception(f"Syntax error at position {e.pos}: {e.text[e.pos:e.pos+20]}") from e
        except Exception as e:
            raise Exception(f"Error parsing expression: {e}") from e
    

if __name__ == "__main__":
    while True:
        grammar = ExpressionGrammar()
        try:
            expr = input("Enter an expression (or 'exit' to quit): ")
            if expr.lower() == "exit":
                break
            ast = grammar(expr)
        except Exception as e:
            print(f"Error: {e}")