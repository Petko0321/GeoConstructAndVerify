# GeoConstructAndVerify

A Python library for constructing and verifying geometric constructions in Euclidean geometry.

## Description

GeoConstructAndVerify is an engine capable of verifying the correctness of geometric constructions introduced through a sequence of primitive or complex steps. The library implements algorithms to compare constructions with original solutions to verify their equivalence, allowing users to determine if a particular construction is correct.

The library uses symbolic computation to represent and manipulate geometric objects and their relationships, enabling precise verification of geometric constructions.

## Installation

```bash
pip install GeoConstructAndVerify
```

Or install from source:

```bash
git clone https://github.com/Petko0321/GeoConstructAndVerify.git
cd GeoConstructAndVerify
pip install -e .
```

## Dependencies

- Python >= 3.6
- sympy >= 1.13.3
- mpmath >= 1.3.0

## Features

- Representation of basic geometric objects (points, lines, circles)
- Implementation of geometric operations (intersection, perpendicular, parallel)
- Verification of construction equivalence
- A collection of geometric utility functions
- Support for both primitive and complex geometric constructions
- Symbolic computation to ensure precise results

## Usage

Here's a simple example of using the library to translate a vector:

```python
from sympy import symbols
from basics import Point, Construction
from utils import Vector, translate

# Create symbolic points
a1, b1, a2, b2, a3, b3 = symbols('a1, b1, a2, b2, a3, b3')
p1 = Point(a1, b1)
p2 = Point(a2, b2)
p3 = Point(a3, b3)

# Initialize the construction
cons = Construction(p1, p2, p3)

# Create a line and vector
line1 = cons.create_line(p1, p2)
v1 = Vector(p1, p2)

# Translate the vector
v2 = translate(v1, p3, optimized=True)

# Print the system
print("Construction system:")
print(cons.system)
```

## Geometric Constructions

The library supports various geometric constructions including:

- Perpendicular bisector
- Angle bisector
- Perpendicular and parallel lines
- Vector translation
- Circle constructions
- And more...

## Examples

The `samples` directory contains numerous examples showcasing the library's capabilities:

- Basic constructions (examples 1-10)
- Verification of equivalence between different construction approaches
- Complex geometric problems and their solutions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
