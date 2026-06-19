# parsimathious

[![PyPI](https://img.shields.io/pypi/v/parsimathious)](https://pypi.org/project/parsimathious/)
[![Python](https://img.shields.io/pypi/pyversions/parsimathious)](https://pypi.org/project/parsimathious/)
[![Tests](https://github.com/stur86/parsimathious/actions/workflows/test.yml/badge.svg)](https://github.com/stur86/parsimathious/actions/workflows/test.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`parsimathious` is a simple mathematical expression parser implemented with [`parsimonious`](https://github.com/erikrose/parsimonious). It supports basic arithmetic operations, parentheses, unary functions, constants, variables, and complex numbers.

## Installation

You can install `parsimathious` using pip:

```bash
pip install parsimathious
```

## Usage

Import the `ExpressionParser` and create an instance:

```python
from parsimathious import ExpressionParser

parser = ExpressionParser()
```

Then you can parse and evaluate expressions:

```python
result = parser("sin(pi / 2) + 1")
print(result)  # Output: 2.0
```

## Supported functions and constants


On top of basic arithmetic operations, `parsimathious` supports the following unary functions and constants by default:

| Name     | Python Implementation           | Description                       |
|----------|--------------------------------|------------------------------------|
| `sin`    | math.sin                       | Sine                               |
| `cos`    | math.cos                       | Cosine                             |
| `tan`    | math.tan                       | Tangent                            |
| `log`    | math.log                       | Natural logarithm (base e)         |
| `sqrt`   | math.sqrt                      | Square root                        |
| `exp`    | math.exp                       | Exponential (e^x)                  |
| `log10`  | math.log10                     | Logarithm base 10                  |
| `abs`    | abs                            | Absolute value                     |
| `floor`  | math.floor                     | Floor (round down)                 |
| `ceil`   | math.ceil                      | Ceiling (round up)                 |
| `round`  | round                          | Round to nearest integer           |
| `sinh`   | math.sinh                      | Hyperbolic sine                    |
| `cosh`   | math.cosh                      | Hyperbolic cosine                  |
| `tanh`   | math.tanh                      | Hyperbolic tangent                 |
| `asin`   | math.asin                      | Arc sine                           |
| `acos`   | math.acos                      | Arc cosine                         |
| `atan`   | math.atan                      | Arc tangent                        |
| `asinh`  | math.asinh                     | Inverse hyperbolic sine            |
| `acosh`  | math.acosh                     | Inverse hyperbolic cosine          |
| `atanh`  | math.atanh                     | Inverse hyperbolic tangent         |
| `sec`    | lambda x: 1 / math.cos(x)      | Secant                             |
| `csc`    | lambda x: 1 / math.sin(x)      | Cosecant                           |
| `cot`    | lambda x: 1 / math.tan(x)      | Cotangent                          |

### Constants

| Name | Value                | Description                |
|------|----------------------|----------------------------|
| `pi` | math.pi              | The mathematical constant π |
| `e`  | math.e               | The mathematical constant e |
| `i`  | 1j                   | The imaginary unit         |

## Custom Unary Functions

It's also possible to support custom unary functions by passing a dictionary of function names to their implementations when creating the `ExpressionParser`:

```python
import math
from parsimathious import ExpressionParser, UnaryFunctionMap

custom_functions: UnaryFunctionMap = {
    "log2": math.log2,  # Logarithm base 2
    "cube": lambda x: x ** 3,  # Cube function
}

parser = ExpressionParser(unary_functions=custom_functions)
result = parser("log2(8) + cube(3)")
print(result)  # Output: 30.0
```

## Custom Constants

Custom constants can be passed via a dictionary of names to values when creating the `ExpressionParser`. This **replaces** the default constants (`pi`, `e`) rather than extending them, so include them again if you still need them:

```python
import math
from parsimathious import ExpressionParser, ConstantMap

custom_constants: ConstantMap = {
    "pi": math.pi,
    "tau": 2 * math.pi,
}

parser = ExpressionParser(constants=custom_constants)
result = parser("tau / pi")
print(result)  # Output: 2.0
```

Constant names cannot overlap with variable names (see below), and `i` is reserved for the imaginary unit and cannot be used as a constant name.

## Variables

Unlike constants, variables don't have a fixed value: their names are declared when creating the `ExpressionParser`, and their values are supplied at evaluation time, by passing a dictionary of names to values to the parser call (or to `eval_ast`):

```python
from parsimathious import ExpressionParser

parser = ExpressionParser(variable_names=["x", "y"])
result = parser("x + y * 2", variables={"x": 1.0, "y": 3.0})
print(result)  # Output: 7.0
```

Each call only uses the variable values passed to it; if an expression references a declared variable but no value is provided for it, a `ValueError` is raised. As with constants, `i` is reserved for the imaginary unit and cannot be used as a variable name, and variable names cannot overlap with constant names.
