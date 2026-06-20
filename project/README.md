# Factor Polynomials
> `x^2 - 3x + 2` <-> `(x - 1)(x - 2)`

A command-line tool for **factoring** and **expanding** polynomials with integer coefficients.

---

## Running
```bash
python polynomial_factory.py
```

Requires Python 3.10+ and standard libraries only (`fractions`, `re`).

---

## User Documentation
### Interactive Mode
Once running, type a polynomial at the `>` prompt. The program automatically detects the mode:

- **no brackets:** factoring: `x^2 - 3x + 2` -> `(x - 1)(x - 2)`
- **brackets:** expanding: `(x - 1)(x - 2)` -> `x^2 - 3x + 2`

Special commands:

| Command | Action |
|---------|--------|
| `file` | load polynomials from a file (one per line) |
| `exit` | quit |

### Valid Input (Standard Form)
```
2x^2 - 3x + 1
x^3 - x^2 + x - 1
6y^2 - 9y + 3
```

| Rule | Valid | Invalid |
|------|-------|---------|
| Coefficients | integers only | `2.5x`, `1/2 x` |
| Variable | one letter (`x`, `y`, `t`, `A`, …) | `xy`, `x1`, `alpha` |
| Multiple variables | not allowed | `x + y` |
| Term order | any | - |
| Spaces | ignored | - |
| `*` for multiplication | `2*x^2`, `2*3x` | `x*y`, `*x`, `x*` |
| Brackets | not allowed in standard form | `(x+1)x` |

**Valid variable names** are any single letter `a`–`z` or `A`–`Z`.

### Valid Input (Factored Form)
```
(x - 1)(x - 2)
2(x - 1)(x - 2)
x(x - 1)
(2x - 1)(3x - 2)
3(y - 1)(2y - 1)
```

The format matches what the factoring mode outputs, so the two modes are fully reversible.

### File Mode
Type `file`, then enter the path to a text file. Each line is processed as a separate polynomial; empty lines are skipped. Lines with comments (e.g. starting with `#`) will be treated as invalid input.

```
> file
Filename: examples.txt
Line 1: x^2 - 3x + 2 = (x - 1)(x - 2)
Line 4: x^2 - x = x(x - 1)
...
```

See the included `examples.txt` for a sample input file.

### Example Outputs (Factoring)
| Input | Output | Note |
|-------|--------|------|
| `x^2 - 3x + 2` | `(x - 1)(x - 2)` | |
| `x^2 - x` | `x(x - 1)` | zero root |
| `2x^2 - 6x + 4` | `2(x - 1)(x - 2)` | leading coefficient |
| `2x^2 - 3x + 1` | `(x - 1)(2x - 1)` | rational root |
| `6x^2 - 7x + 2` | `(2x - 1)(3x - 2)` | rational roots |
| `x^3 - x^2 + x - 1` | `(x - 1)(x^2 + 1)` | irreducible factor |
| `x^2 + 1` | `(x^2 + 1)` | irreducible |
| `5` | `5` | constant |
| `x - x` | `0` | zero polynomial |

### Example Outputs (Expanding)
| Input | Output |
|-------|--------|
| `(x - 1)(x - 2)` | `x^2 - 3x + 2` |
| `2(x - 1)(x - 2)` | `2x^2 - 6x + 4` |
| `(x - 1)(x^2 + 1)` | `x^3 - x^2 + x - 1` |

---

## Technical Documentation
### Architecture
```
Input Parsing -> Factor Polynomial -> [output]

Expand Polynomial  (separate pipeline, shares helpers)
```

The program has four logical sections:

1. **Input Parsing:** converts a string into an internal polynomial representation
2. **Factor Polynomial:** applies the rational root theorem to find factors
3. **Expand Polynomial:** multiplies bracketed factors back into standard form
4. **Overhead:** keyboard loop and file processing

### Internal Representation
A polynomial is stored as `dict[int, int]` mapping power -> coefficient:

```
2x^2 - 3x + 1  ->  {2: 2, 1: -3, 0: 1}
```

Alternatively as `list[int]`, coefficients from highest to lowest power:

```
2x^2 - 3x + 1  ->  [2, -3, 1]
```

The dict form is used for arithmetic, whilst the array form is used for the factoring algorithm.

### Factoring Algorithm
1. Convert the polynomial to coefficient array form.
2. Apply the **[rational root theorem](https://en.wikipedia.org/wiki/Rational_root_theorem)**: candidates are all fractions `p/q` where `p` divides the constant term and `q` divides the leading coefficient.
3. Test each candidate using **[Horner's scheme](https://en.wikipedia.org/wiki/Horner%27s_method)**.
4. For each confirmed root, divide the polynomial by `(x - r)` via `deflate` and repeat on the reduced polynomial.
5. Any remaining degree-≥2 polynomial with no rational roots is kept as an irreducible factor.

### Error Handling
All errors are raised as `ValueError` with a descriptive message:

| Situation | Example input | Error message |
|-----------|--------------|---------------|
| Empty input | `""` | `Input polynomial cannot be empty` |
| Decimal coefficient | `2.5x^2` | `Only integer coefficients are supported, got '2.5x^2'` |
| Multiple variables | `x + y` | `You cannot use more than one variable` |
| Misplaced `*` | `2x +* 1` | `Invalid use of '*' in '2x +* 1'` |
| Malformed term | `2x3` | `Malformed term: '2x3'` |
| File not found | *(bad path)* | `File '<path>' not found` |

### Limitations
- Input coefficients must be **integers**.
- Only **rational roots** are found, `x^2 + x + 1` stays as `(x^2 + x + 1)`.
- Only **one variable** per polynomial.
- Polynomial **parameters** in coefficients are not supported (e.g. `ax^2 + b`).
- File mode does **not** support comments.