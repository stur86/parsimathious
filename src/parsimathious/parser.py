import math
from typing import Any, Sequence

from parsimonious import NodeVisitor
from parsimonious.nodes import Node
from .grammar import ExpressionGrammar, UnaryFunctionMap, _DEFAULT_UNARY_FUNCTIONS


class ExpressionVisitor(NodeVisitor):
    unwrapped_exceptions = (ValueError,)

    def __init__(self, unary_functions: UnaryFunctionMap):
        super().__init__()
        self._unary_functions = unary_functions
        self._variable_values: dict[str, float | complex] = {}

    def visit_complex_number(self, node, visited_children):
        return visited_children[0]
        
    def visit_imaginary_number(self, node, visited_children):
        number_node, _ = visited_children
        if number_node is None:
            return complex(0, 1)  # Just "i" means 0 + 1i
        else:
            return complex(0, float(number_node))  # e.g., "2i" means 0 + 2i
        
    def visit_number(self, node, visited_children):
        return float(node.text)
    
    def visit_imaginary_unit(self, node, visited_children):
        return 1.0j
    
    def visit_constant(self, node, visited_children):
        constant_map = {
            "pi": math.pi,
            "e": math.e,
        }
        try:
            return constant_map[node.text]
        except KeyError:
            raise ValueError(f"Unknown constant: {node.text}")

    def visit_variable(self, node, visited_children):
        try:
            return self._variable_values[node.text]
        except KeyError:
            raise ValueError(f"No value provided for variable: {node.text}")

    def visit_atom(self, node, visited_children):
        return visited_children[0]
    
    def visit_exp_factor(self, node, visited_children):
        return visited_children[0]
    
    def visit_factor(self, node, visited_children):
        base = visited_children[0]
        for op, exponent in visited_children[1]:
            if op.text != "^":
                raise ValueError(f"Unexpected operator in factor: {op.text}")
            base = base ** exponent
        return base
    
    def visit_term(self, node, visited_children):
        result = visited_children[0]
        for [op], factor in visited_children[1]:
            if op.text == "*":
                result *= factor
            elif op.text == "/":
                result /= factor
            else:
                raise ValueError(f"Unexpected operator in term: {op.text}")
        return result
    
    def visit_sum(self, node, visited_children):
        result = visited_children[0]
        for [op], term in visited_children[1]:
            if op.text == "+":
                result += term
            elif op.text == "-":
                result -= term
            else:
                raise ValueError(f"Unexpected operator in expression: {op.text}")
        return result
    
    def visit_parenthesized_expression(self, node, visited_children):
        _, expr, _ = visited_children
        return expr[0]
    
    def visit_function_name(self, node, visited_children):
        return node
    
    def visit_function_call(self, node, visited_children):
        function_name_node, arg_node = visited_children
        function_name = function_name_node.text
        if function_name not in self._unary_functions:
            raise ValueError(f"Unknown function: {function_name}")
        func = self._unary_functions[function_name]
        arg_value = arg_node  # The argument is the first child of the parenthesized expression
        return func(arg_value)
            
    def generic_visit(self, node: Node, visited_children: Sequence[Any]):
        return visited_children or node
    
class ExpressionParser:
    def __init__(
        self,
        unary_functions: UnaryFunctionMap = _DEFAULT_UNARY_FUNCTIONS,
        variable_names: Sequence[str] = (),
    ):
        """
        Initialize the ExpressionParser with optional unary functions and variable names.

        Args:
            unary_functions (UnaryFunctionMap): A dictionary mapping function names to their implementations.
            variable_names (Sequence[str]): Names of variables that may appear in expressions. Their values
                are supplied at evaluation time rather than at construction time.
        """
        self._grammar = ExpressionGrammar(unary_functions, variable_names)
        self._visitor = ExpressionVisitor(unary_functions)

    def compute_ast(self, expression: str) -> Node:
        """Compute the abstract syntax tree (AST) for the given expression.
        
        Args:
            expression (str): The mathematical expression to parse.
        
        Returns:
            Node: The abstract syntax tree (AST) representing the expression.
        """
        return self._grammar(expression)
    
    def eval_ast(self, ast: Node, variables: dict[str, float | complex] | None = None) -> float | complex:
        """Evaluate the given abstract syntax tree (AST) and return the result.

        Args:
            ast (Node): The abstract syntax tree (AST) to evaluate.
            variables (dict[str, float | complex] | None): Values for any variable names declared on
                construction. Only needed if the expression references variables.

        Returns:
            float | complex: The result of evaluating the AST.
        """
        self._visitor._variable_values = variables or {}
        try:
            return self._visitor.visit(ast)
        finally:
            self._visitor._variable_values = {}

    def __call__(self, expression: str, variables: dict[str, float | complex] | None = None) -> float | complex:
        ast = self.compute_ast(expression)
        return self.eval_ast(ast, variables)