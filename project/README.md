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

---

### Functions
#### Input Parsing
**splitTerms(polynomial: str) -> list[str]**  
- checks whether the input is in standard polynomial form
- trims spaces
- resolves `2*3x` → `6x` and strips valid `*` between coefficients and variables
- splits terms into an array
- validates that all coefficients are integers
- returns array in the opposite order as it is more effective to handle sign operators (+/-) that way
```python
splitTerms("+18 + 19 + x^5")  # ["x^5", "19", "18"]
```

**getVariable(terms: list[str]) -> str**  
- checks whether only a single letter (uppercase or lowercase) is used as a variable
- returns that letter
- if no letter is found, returns `x`
```python
getVariable(["13", "-21x"])  # "x"
```

**sumTerms(var: str, terms: list[str]) -> dict[int, int]**  
- first handles absolute and linear terms as they are different from other terms
- adds leading 1s to existing terms without explicit coefficient
- splits into sets of coefficient, power
- checks for malformed terms
- saves power as a key to the dict and adds the coefficients to it, accumulating if the power already exists
```python
sumTerms("x", ["-15", "2x", "3x^12", "-x"])  # {12: 3, 1: 1, 0: -15}
```

**normalizeDict(polDict: dict[int, int]) -> dict[int, int]**  
- from the dict, deletes all entries with value of 0
```python
normalizeDict({2: 1, 1: 0, 0: -3})  # {2: 1, 0: -3}
```

**parseInput(polynomial: str) -> tuple[dict[int, int], str]**  
- overhead function combining `splitTerms()`, `getVariable()`, `sumTerms()` and finally `normalizeDict()`
```python
parseInput("x^2 - 3x + 1")  # ({2: 1, 1: -3, 0: 1}, "x")
```

#### Factor Polynomial
**dictToArray(polDict: dict[int, int]) -> list[int]**  
- handles empty dictionary
- transforms dict into array of coefficients with zero for missing powers
```python
dictToArray({3: 2, 1: -1, 0: 5})  # [2, 0, -1, 5]
```

**findCandidates(polArray: list[int]) -> list[tuple[int, int]]**  
- deletes trailing zeros and adds 0 as a root of the polynomial
- finds divisors of absolute and leading coefficient
- using Rational root theorem, finds all candidates for rational roots
```python
set(findCandidates([2, -3, 1]))  # {(1, 1), (-1, 1), (1, 2), (-1, 2)}
```

**horner(polArray: list[int], candidate: tuple[int, int]) -> bool**  
- tests candidate for root of a polynomial using Horner's scheme
```python
horner([1, -3, 2], (2, 1))  # True
```

**deflate(polArray: list[int], root: tuple[int, int]) -> list[int]**  
- divides polynomial by its root using Horner's scheme
- checks whether remainder is zero (if not throws an error)
```python
deflate([1, -3, 2], (2, 1))  # [1, -1]
```

**getIrreducible(polArray: list[int], var: str) -> str**  
- returns an empty string for a single-element array as the case is handled elsewhere
- iterates over coefficients, tracking the current power
- skips zero coefficients entirely
- handles the sign of the leading term separately (no leading `+`) and adds ` + ` / ` - ` between later terms using `signum()`
- suppresses the coefficient `1` when the power is greater than zero (writes `x` not `1x`)
- formats each term according to its power: `x^n` for n > 1, `x` for n == 1, bare number for n == 0
```python
getIrreducible([1, 0, 1], "x")  # "x^2 + 1"
```

**signum(number: int) -> str**  
- series of if / else statements checking whether the number is positive, negative, or neither
```python
signum(5)   # "+"
signum(-3)  # "-"
signum(0)   # ""
```

**factorPolynomial(initTuple: tuple[dict[int, int], str]) -> str**  
- unpacks the dict and variable, converts dict to array form
- returns immediately for constant polynomials
- iterates over candidates, using Horner's scheme to confirm roots and deflating the polynomial after each one found; a `while` loop handles repeated roots
- computes the scalar factor as the leading coefficient divided by the product of all root denominators
- assembles the output string: optional scalar, then one bracket per root (`x` for a zero root, `(x ± p)` for integer roots, `(qx ± p)` for fractional ones), and finally the irreducible remainder if any is left over
```python
factorPolynomial(({2: 6, 1: -9, 0: 3}, "x"))  # "3(x - 1)(2x - 1)"
```

#### Expand Polynomial
**multiplyPolDicts(pol1: dict[int, int], pol2: dict[int, int]) -> dict[int, int]**  
- iterates over every pair of terms from both polynomials
- multiplies the two coefficients and adds the two powers to get the new term
- accumulates the result in a fresh dict, summing into an existing key when the same power appears more than once
```python
multiplyPolDicts({1: 1, 0: -1}, {1: 1, 0: -2})  # {2: 1, 1: -3, 0: 2}
```

**polDictToStr(polDict: dict[int, int], var: str) -> str**  
- handles zero polynomial by returning `"0"`
- converts the dict to array form and delegates formatting to `getIrreducible()`
```python
polDictToStr({2: 1, 1: -3, 0: 2}, "x")  # "x^2 - 3x + 2"
```

**expandPolynomial(factored: str) -> str**  
- strips spaces and handles the zero polynomial as a special case
- detects the variable from the first letter found in the string using regex
- starts with the multiplicative identity `{0: 1}` and optionally replaces it with a leading scalar
- handles a bare variable at the front of the string (representing a zero root) by multiplying in `{1: 1}`
- parses each parenthesised factor in turn using `parseInput()` and multiplies it into the running product with `multiplyPolDicts()`
- normalises and converts the result back to a string with `polDictToStr()`
```python
expandPolynomial("(x - 1)(x - 2)")  # "x^2 - 3x + 2"
```

#### Overhead
**grandOrchestrator(polynomial: str) -> str**  
- overhead function combining `parseInput()` and `factorPolynomial()`
```python
grandOrchestrator("2x^2 - 6x + 4")  # "2(x - 1)(x - 2)"
```

**processFile(filename: str) -> None**  
- opens file
- trims spaces and skips empty lines
- evaluates each line using `grandOrchestrator()` and prints the result alongside its line number
- handles errors per line without aborting the whole file

**keyboardLoop() -> None**  
- runs an interactive loop in the terminal, letting the user factor or expand polynomials until deliberately closed
- routes inputs containing parentheses to `expandPolynomial()` and all others to `grandOrchestrator()`