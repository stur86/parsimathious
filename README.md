# parsimathious

`parsimathious` is a simple mathematical expression parser implemented with [`parsimonious`](https://github.com/erikrose/parsimonious). It supports basic arithmetic operations, parentheses, unary functions, constants, and complex numbers.

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
print(result)  # Output: 35.0
```
