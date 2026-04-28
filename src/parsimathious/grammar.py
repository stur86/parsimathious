import math
from parsimonious import Grammar
from parsimonious.nodes import Node
from typing import Dict, Callable

_UnaryFunction = Callable[[float], float]
_UnaryFunctionMap = Dict[str, _UnaryFunction]

_DEFAULT_UNARY_FUNCTIONS: _UnaryFunctionMap = {
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
    
    def __init__(self, unary_functions: _UnaryFunctionMap = _DEFAULT_UNARY_FUNCTIONS):
        if len(unary_functions) == 0:
            raise ValueError("At least one unary function must be provided.")
        function_names = " / ".join(f'"{name}"' for name in unary_functions.keys())
        self._grammar = Grammar(f"""
            expression = term (add_op term)*
            term = factor (mul_op factor)*
            factor = exp_factor (exp_op exp_factor)*
            exp_factor = unary_op? atom
            atom = number / function_call / parenthesized_expression
            function_call = function_name parenthesized_expression
            parenthesized_expression = "(" expression ")"
            add_op = "+" / "-"
            mul_op = "*" / "/"
            exp_op = "^"
            unary_op = "+" / "-"
            number = ~r"\\d+(\\.\\d+)?"
            function_name = {function_names}
        """)

    def __call__(self, expression: str) -> Node:
        return self._grammar.parse(expression)
    

if __name__ == "__main__":
    while True:
        grammar = ExpressionGrammar()
        try:
            expr = input("Enter an expression (or 'exit' to quit): ")
            if expr.lower() == "exit":
                break
            ast = grammar(expr)
            print(ast)
        except Exception as e:
            print(f"Error: {e}")