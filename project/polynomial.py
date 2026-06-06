#

#! Import
from fractions import Fraction
import re


#! Input Parsing
#* Split terms
def splitTerms(polynomial: str) -> list[str]:
    """
    Checks whether input satisfies standard polynomial form, if so splits it into individual terms

    Input: string including polynomial

    Output: array of terms of the polynomial

    Note: returns terms in reverse order, depends on re (regex) library
    """

    # delete spaces and check for empty string
    spaceless = polynomial.replace(" ", "")

    if not spaceless:
        raise ValueError("Input polynomial cannot be empty")
    
    # multiply numbers with star
    def multiplyMatch(match):
        left = int(match.group(1))
        right = int(match.group(2))
        return str(left * right)

    while re.search(r'(\d+)\*(\d+)', spaceless):
        spaceless = re.sub(r'(\d+)\*(\d+)', multiplyMatch, spaceless)

    # delete valid stars
    for i, char in enumerate(spaceless):
        if char == "*":
            if i == 0 or i == len(spaceless) - 1:
                raise ValueError(f"Invalid use of '*' in '{polynomial}'")
            if not (spaceless[i-1].isdigit() and spaceless[i+1].isalpha()):
                raise ValueError(f"Invalid use of '*' in '{polynomial}'")

    starless = spaceless.replace("*", "")

    # add operator to the start
    if starless[0] not in ["+", "-"]:
        starless = "+" + starless

    # split terms
    terms = []
    currentLength = 0

    for i, char in enumerate(reversed(starless)):
        currentLength += 1

        if char in ["+", "-"]:
            startIndex = len(starless) - i
            endIndex = len(starless) - i + currentLength

            if char == "+":
                terms.append(starless[startIndex:endIndex-1])
            elif char == "-":
                terms.append(starless[startIndex - 1:endIndex-1])

            currentLength = 0

    terms = [t for t in terms if t]

    # validate terms
    for term in terms:
        if '.' in term or "," in term:
            raise ValueError(f"Only integer coefficients are supported, got '{term}'")
    
    validTerm = re.compile(r'^-?(\d+[a-zA-Z]?|[a-zA-Z])(\^\d+)?$')
    for term in terms:
        if not validTerm.match(term):
            raise ValueError(f"Malformed term: '{term}'")
    
    # return
    return terms


#* Get variable
def getVariable(terms: list[str]) -> str:
    """
    Input: array of terms of the polynomial

    Output: string of one character

    Note: currently the polynomials only support a single variable defined by a single char letter,
    and do not support parameters.
    """

    var = None

    for term in terms:
        for char in term:
            if char.isalpha():
                if var is None:
                    var = char
                elif var != char:
                    raise ValueError("You cannot use more than one variable")

    if var is None:
        var = "x"

    return var


#* Sum terms
def sumTerms(var: str, terms: list[str]) -> dict[int, int]:
    """
    Inputs: variable of polynomial (char) & array of terms of the polynomial

    Output: dict, where keys are powers (int) of the variable and values are their coefficients (int)
    """

    powers = {}

    for term in terms:
        # absolute & linear terms
        if "^" not in term:
            if var in term:
                term += "^1"
            else:
                term += f"{var}^0"
        
        # add leading 1s
        if term[0] == var:
            term = "1" + term
        elif term.startswith(f"-{var}"):
            term = "-1" + term[1:]

        # split into coefficient & power
        parts = term.split(f"{var}^")

        if len(parts) != 2:
            raise ValueError(f"Malformed term: '{term}'")

        try:
            coef = int(parts[0])
            power = int(parts[1])
        except ValueError:
            raise ValueError(f"Malformed term — expected integer coefficient and power, got '{term}'")

        # add to dictionary
        if power not in powers:
            powers[power] = 0

        powers[power] += coef
    return powers


#* Normalize dictionary
def normalizeDict(polDict: dict[int, int]) -> dict[int, int]:
    """
        Deletes all entries in the dictionary with value 0

        Input: dict, where keys are powers (int) of the variable and values are their coefficients (int)

        Output: dict, where keys are powers (int) of the variable and values are their coefficients (int)
    """

    newPolDict = {}
    for power, coef in polDict.items():
        if coef != 0:
            newPolDict[power] = coef

    return newPolDict


#* Parse input
def parseInput(polynomial: str) -> tuple[dict[int, int], str]:
    """
    Input: string including polynomial

    Output: tuple containing dict (where keys are powers (int) of the variable and values are their coefficients (int)) and a variable (string)
    """

    terms = splitTerms(polynomial)
    var = getVariable(terms)
    return (normalizeDict(sumTerms(var, terms)), var)


#! Factor Polynomial
#* Dict to array
def dictToArray(polDict: dict[int, int]) -> list[int]:
    """
    Transforms the dict representation of polynomial into the array representation of it.

    Input: dict, where keys are powers (int) of the variable and values are their coefficients (int)

    Output: array of coefficients from the highest power descending to the absolute term

    Note: empty dictionary is taken as 0 polynomial
    """

    # empty dict
    if polDict == {}:
        return [0]
    
    polArray = []
    previousPower = None

    # transform dict into array with zero coef for missing powers
    for power, coef in sorted(polDict.items(), reverse=True):
        if previousPower is None:
            polArray.append(coef)
        elif previousPower - power == 1:
            polArray.append(coef)
        else:
            for _ in range(previousPower - power - 1):
                polArray.append(0)
            polArray.append(coef)

        previousPower = power

    # add trailing zeros
    if previousPower != 0:
        for _ in range(previousPower):
                polArray.append(0)

    return polArray


#* Find candidate roots
def findCandidates(polArray: list[int]) -> list[tuple[int, int]]:
    """
    Finds all candidates for roots based on Rational root theorem

    Input: array of coefficients from the highest power descending to the absolute term

    Output: array of tuples representing fractions
    """

    candidates = []

    # delete trailing zeros
    hasZeroRoot = False
    
    while polArray[-1] == 0 and len(polArray) > 1:
        polArray = polArray[:-1]
        hasZeroRoot = True

    if hasZeroRoot:
        candidates.append((0, 1))

    # divisors of absolute coef
    absCoef = abs(polArray[-1])
    absCoefDivisors = []

    for n in range(1, absCoef // 2 + 1):
        if absCoef % n == 0:
            absCoefDivisors.append(n)

    absCoefDivisors.append(absCoef)

    # divisors of leading coef
    leadCoef = abs(polArray[0])
    leadCoefDivisors = []

    for n in range(1, leadCoef // 2 + 1):
        if leadCoef % n == 0:
            leadCoefDivisors.append(n)

    leadCoefDivisors.append(leadCoef)

    # candidates
    for leadDivisor in leadCoefDivisors:
        for absDivisor in absCoefDivisors:
            candidates.append((absDivisor, leadDivisor))
            candidates.append((-absDivisor, leadDivisor))
    return candidates


#* Horner's scheme
def horner(polArray: list[int], candidate: tuple[int, int]) -> bool:
    """
    Finds whether a candidate is a root of the polynomial

    Input: polynomial (array of coefficients from the highest power descending to the absolute term)
    and a single candidate depicted by a tuple (p, q) representing a fraction p/q

    Output: boolean value where True implies candidate is root and False means it's not

    Note: This function depends on fractions library
    """

    result = polArray[0]
    x = Fraction(candidate[0], candidate[1])

    for coef in polArray[1:]:
        result = result * x + coef

    return result == 0


#* Deflate polynomial
def deflate(polArray: list[int], root: tuple[int, int]) -> list[int]:
    """
    Divides polynomial by its root using Horner's scheme

    Input: polynomial (array of coefficients from the highest power descending to the absolute term) and its root

    Output: polynomial (in array form) divided by (r - x)

    Note: This function depends on fractions library
    """

    # get coefs of deflated polynomial
    result = polArray[0]
    x = Fraction(root[0], root[1])
    newPolArray = [result]

    for coef in polArray[1:-1]:
        result = result * x + coef
        newPolArray.append(result)
    
    # check whether remainder is zero
    result = result * x + polArray[-1]

    if result != 0:
        raise ValueError("deflate() was expecting a root of a polynomial")

    # return
    return [int(z) for z in newPolArray]


#* Get irreducible factor
def getIrreducible(polArray: list[int], var: str) -> str:
    """
    Transforms array representing irreducible factor into a string

    Input: array of coefficients from the highest power descending to the absolute term

    Output: string including irreducible term of a polynomial
    """

    irreducible = ""

    if len(polArray) > 1:
        power = len(polArray) - 1

        for coef in polArray:
            if coef != 0:
                if irreducible == "" and signum(coef) == "-":
                    irreducible += "-"
                elif irreducible != "":
                    if signum(coef) == "+":
                        irreducible += " + "
                    else:
                        irreducible += " - "
                
                coefStr = "" if abs(coef) == 1 and power > 0 else str(abs(coef))

                if power > 1:
                    irreducible += f"{coefStr}{var}^{power}"
                elif power == 1:
                    irreducible += f"{coefStr}{var}"
                elif power == 0:
                    irreducible += f"{abs(coef)}"
            
            power -= 1
    return irreducible


#* Signum
def signum(number: int) -> str:
    """
    Returns a string of +, - or "" based on the sign of the input integer
    """

    if number > 0:
        return "+"
    elif number < 0:
        return "-"
    else:
        return ""


#* Factor polynomial
def factorPolynomial(initTuple: tuple[dict[int, int], str]) -> str:
    """
    Input: tuple containing dict (where keys are powers (int) of the variable and values are their coefficients (int)) and a variable (string)

    Output: string of the factored polynomial
    """

    # initialization
    polDict = initTuple[0]
    var = initTuple[1]

    polArray = dictToArray(polDict)
    candidates = findCandidates(polArray)
    leadingCoef = polArray[0]
    factoredPol = ""

    # check for constant polynom
    if len(polArray) == 1:
        return str(polArray[0])

    # get roots
    roots = []

    for candidate in candidates:
        while horner(polArray, candidate):
            roots.append(candidate)
            polArray = deflate(polArray, candidate)

        if len(polArray) == 1:
            break

    # get leading coefficient
    if roots:
        denomProduct = 1
        for root in roots:
            denomProduct *= root[1]
        scalar = leadingCoef // denomProduct

        if scalar != 1:
            factoredPol += str(scalar)

    # rewrite in bracket notation
    irreducible = getIrreducible(polArray, var)

    for root in roots:
        if root[0] == 0:
            factoredPol += var
        elif root[1] == 1:
            factoredPol += f"({var} {signum(-root[0])} {abs(root[0])})"
        else:
            factoredPol += f"({root[1]}{var} {signum(-root[0])} {abs(root[0])})"

    if irreducible != "":
        factoredPol += f"({irreducible})"

    return factoredPol


#! Overhead Functions
#* The grand orchestrator
def grandOrchestrator(polynomial: str) -> str:    
    return factorPolynomial(parseInput(polynomial))


#* Process file
def processFile(filename: str) -> None:
    """
    Reads polynomials from a file, one per line, and prints factored results.

    Input: path to a text file

    Output: None (prints to console)
    """

    # open file
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        raise ValueError(f"File '{filename}' not found")
    except OSError:
        raise ValueError(f"Could not read file '{filename}'")

    # prepare lines
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        # evaluate line
        try:
            result = grandOrchestrator(stripped)
            print(f"Line {i}: {stripped} = {result}")
        except ValueError as e:
            print(f"Line {i}: invalid input ({e})")


#* Keyboard loop

def keyboardLoop() -> None:
    """
    Repeatedly reads polynomials from keyboard input and prints factored results.
    Type 'file' to process a file, 'exit' to quit.
    """

    print("Polynomial Factory©")
    print(" ✨brought to you by Kotvič✨\n")
    print("Type 'file' to load from file, 'exit' to quit\n")

    while True:
        pol = input("> ").strip()

        if not pol:
            continue
        elif pol == "exit":
            break
        elif pol == "file":
            filename = input("Filename: ").strip()
            try:
                processFile(filename)
            except ValueError as e:
                print(f"Error: {e}")
        else:
            try:
                if "(" in pol:
                    result = expandPolynomial(pol)
                else:
                    result = grandOrchestrator(pol)
                print(f"= {result}\n")
            except ValueError as e:
                print(f"Invalid input: {e}\n")


#! Expand Polynomial
#* Multiply polynomial dictionaries
def multiplyPolDicts(pol1: dict[int, int], pol2: dict[int, int]) -> dict[int, int]:
    """
    Multiplies two polynomials in dict representation.

    Input: two dicts where keys are powers (int) and values are coefficients (int)

    Output: dict of the product
    """

    result = {}

    for power1, coef1 in pol1.items():
        for power2, coef2 in pol2.items():
            newPower = power1 + power2
            result[newPower] = result.get(newPower, 0) + coef1 * coef2

    return result


#* Polynomial dictionary to string
def polDictToStr(polDict: dict[int, int], var: str) -> str:
    """
    Converts a polynomial dict into a string.

    Input: dictionary where keys are powers (int) and values are coefficients (int), and variable (str)

    Output: string representation of the polynomial
    """

    # zero polynomial
    if not polDict:
        return "0"

    polArray = dictToArray(polDict)

    # constant case (skipped by getIrreducible)
    if len(polArray) == 1:
        return str(polArray[0])

    return getIrreducible(polArray, var)


#* Expand polynomial
def expandPolynomial(factored: str) -> str:
    """
    Expands a factored polynomial string back into standard form.

    Input: string in factored form (as produced by factorPolynomial)

    Output: string in standard polynomial form
    """

    # zero polynomial
    if factored == "0":
        return "0"

    # detect variable
    varMatch = re.search(r'[a-zA-Z]', factored)
    var = varMatch.group() if varMatch else "x"

    # multiplicative identity - one
    result = {0: 1}
    remaining = factored

    # extract leading scalar
    scalarMatch = re.match(r'^(-?\d+)', remaining)

    if scalarMatch:
        result = {0: int(scalarMatch.group(1))}
        remaining = remaining[scalarMatch.end():]

    # extract bare variable (zero root)
    if remaining.startswith(var):
        result = multiplyPolDicts(result, {1: 1})
        remaining = remaining[1:]

    # extract and multiply each bracketed factor
    while remaining.startswith("("):
        depth = 0

        for i, char in enumerate(remaining):
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1

                if depth == 0:
                    factorDict, _ = parseInput(remaining[1:i])
                    result = multiplyPolDicts(result, factorDict)
                    remaining = remaining[i + 1:]
                    break

    return polDictToStr(normalizeDict(result), var)


#! Tests
def test():
    #* Split terms
    assert splitTerms("-21x + 13") == ["13", "-21x"]
    assert splitTerms("-1") == ["-1"]
    assert splitTerms("+18 + 19 + x^5") == ["x^5", "19", "18"]
    assert splitTerms("0 + x") == ["x", "0"]
    assert splitTerms("  -21     x+  13 ") == ["13", "-21x"]
    assert splitTerms("-42") == ["-42"]
    assert splitTerms("x^2 - 3x + 1") == ["1", "-3x", "x^2"]
    assert splitTerms("2*x^2 + 3*x - 5") == splitTerms("2x^2 + 3x - 5")
    assert splitTerms("2*3x^2") == splitTerms("6x^2")

    try:
        splitTerms("2x +* 1")
        assert False
    except ValueError:
        assert True

    try:
        splitTerms("2.5x^2 + 1")
        assert False
    except ValueError as e:
        assert "integer" in str(e)

    #* Get variable
    assert getVariable(["13", "-21x"]) == "x"
    assert getVariable(["15", "1"]) == "x"
    assert getVariable(["15", "101x^15"]) == "x"
    assert getVariable(["19x", "2x^2"]) == "x"

    try:
        getVariable(["2x", "13y^2", "2"])
        assert False
    except ValueError:
        assert True

    #* Sum terms
    assert sumTerms("x", ["2x^2", "3x", "-5"]) == {2: 2, 1: 3, 0: -5}
    assert sumTerms("x", ["5", "3", "-2"]) == {0: 6}
    assert sumTerms("x", ["7x^3"]) == {3: 7}
    assert sumTerms("x", ["x", "x", "-x"]) == {1: 1}
    assert sumTerms("x", ["-15", "2x", "3x^12", "-x"]) == {12: 3, 1: 1, 0: -15}
    assert sumTerms("x", ["2x", "-2x"]) == {1: 0}
    assert sumTerms("x", ["3x^2", "5x^2", "-2x"]) == {2: 8, 1: -2}

    try:
        sumTerms("x", ["2x3"])
        assert False
    except ValueError:
        assert True

    try:
        sumTerms("x", ["2.5x^2"])
        assert False
    except ValueError:
        assert True

    #* Parse input
    assert parseInput("x^2 - 3x + 1") == ({2: 1, 1: -3, 0: 1}, "x")
    assert parseInput("-x^2 + 3x - 1") == ({2: -1, 1: 3, 0: -1}, "x")
    assert parseInput("5") == ({0: 5}, "x")
    assert parseInput("x") == ({1: 1}, "x")
    assert parseInput("-x") == ({1: -1}, "x")
    assert parseInput("x - x") == ({}, "x")
    assert parseInput("2y^2 - y + 3") == ({2: 2, 1: -1, 0: 3}, "y")
    assert parseInput("3x + 2x - 5") == ({1: 5, 0: -5}, "x")

    try:
        parseInput("x + y")
        assert False
    except ValueError:
        assert True

    #* Dict to array
    assert dictToArray({3: 2, 2: 3, 1: -1, 0: 5}) == [2, 3, -1, 5]
    assert dictToArray({3: 2, 1: -1, 0: 5}) == [2, 0, -1, 5]
    assert dictToArray({5: 2, 3: -1, 0: 4}) == [2, 0, -1, 0, 0, 4]
    assert dictToArray({0: 7}) == [7]
    assert dictToArray({3: 2}) == [2, 0, 0, 0]
    assert dictToArray({6: 1, 0: 2}) == [1, 0, 0, 0, 0, 0, 2]
    assert dictToArray({0: 5, 3: 2, 1: -1}) == [2, 0, -1, 5]
    assert dictToArray({}) == [0]

    #* Find candidates
    assert findCandidates([1, -3, 2]) == [(1, 1), (-1, 1), (2, 1), (-2, 1)]
    assert findCandidates([1, -5, 6]) == [(1, 1), (-1, 1), (2, 1), (-2, 1), (3, 1), (-3, 1), (6, 1), (-6, 1)]
    assert findCandidates([2, -3, 1]) == [(1, 1), (-1, 1), (1, 2), (-1, 2)]
    assert findCandidates([6, -11, 6, -1]) == [(1, 1), (-1, 1), (1, 2), (-1, 2), (1, 3), (-1, 3), (1, 6), (-1, 6)]
    assert findCandidates([1, -1, 0]) == [(0, 1), (1, 1), (-1, 1)]
    assert findCandidates([1, 0, 0, 0]) == [(0, 1), (1, 1), (-1, 1)]
    assert findCandidates([1]) == [(1, 1), (-1, 1)]
    assert findCandidates([2, 1, -6]) == [(1, 1), (-1, 1), (2, 1), (-2, 1), (3, 1), (-3, 1), (6, 1), (-6, 1), (1, 2), (-1, 2), (2, 2), (-2, 2), (3, 2), (-3, 2), (6, 2), (-6, 2)]

    #* Horner's scheme
    assert horner([1, -3, 2], (1, 1))
    assert horner([1, -3, 2], (2, 1))
    assert not horner([1, -3, 2], (3, 1))
    assert horner([2, -3, 1], (1, 2))
    assert horner([1, -1, 0], (0, 1))
    assert not horner([5], (1, 1))

    #* Deflate polynomial
    assert deflate([1, -3, 2], (1, 1)) == [1, -2]
    assert deflate([1, -3, 2], (2, 1)) == [1, -1]
    assert deflate([2, -3, 1], (1, 2)) == [2, -2]
    assert deflate([1, -6, 11, -6], (1, 1)) == [1, -5, 6]

    try:
        deflate([1, -3, 2], (3, 1))
        assert False
    except ValueError:
        assert True

    #* Get irreducible factor
    assert getIrreducible([1, -1], "x") == "x - 1"
    assert getIrreducible([1, 1], "x") == "x + 1"
    assert getIrreducible([-1, 1], "x") == "-x + 1"
    assert getIrreducible([1, 0, 1], "x") == "x^2 + 1"
    assert getIrreducible([1, -3, 2], "x") == "x^2 - 3x + 2"
    assert getIrreducible([1], "x") == ""
    assert getIrreducible([1, -1], "y") == "y - 1"
    assert getIrreducible([1, 0, 1], "y") == "y^2 + 1"

    #* Factor polynomial
    assert factorPolynomial(({2: 1, 1: -2, 0: 1}, "x")) == "(x - 1)(x - 1)"
    assert factorPolynomial(({2: 1, 1: 3, 0: 2}, "x")) == "(x + 1)(x + 2)"
    assert factorPolynomial(({3: 1, 2: -1, 1: 1, 0: -1}, "x")) == "(x - 1)(x^2 + 1)"
    assert factorPolynomial(({2: 1, 1: -1, 0: 0}, "x")) == "x(x - 1)"
    assert factorPolynomial(({2: 2, 1: -6, 0: 4}, "x")) == "2(x - 1)(x - 2)"
    assert factorPolynomial(({2: 2, 1: -3, 0: 1}, "x")) == "(x - 1)(2x - 1)"
    assert factorPolynomial(({2: 6, 1: -7, 0: 2}, "x")) == "(2x - 1)(3x - 2)"
    assert factorPolynomial(({2: 6, 1: -9, 0: 3}, "x")) == "3(x - 1)(2x - 1)"
    assert factorPolynomial(({2: 2, 1: -1, 0: 3}, "y")) == "(2y^2 - y + 3)"
    assert factorPolynomial(({2: 1, 1: -3, 0: 2}, "y")) == "(y - 1)(y - 2)"
    assert factorPolynomial(({2: 6, 1: -9, 0: 3}, "y")) == "3(y - 1)(2y - 1)"
    assert factorPolynomial(({0: 5}, "x")) == "5"

    #* The grand orchestrator
    assert grandOrchestrator("x^2 - 3x + 2") == "(x - 1)(x - 2)"
    assert grandOrchestrator("2x^2 - 6x + 4") == "2(x - 1)(x - 2)"
    assert grandOrchestrator("x^3 - x^2 + x - 1") == "(x - 1)(x^2 + 1)"
    assert grandOrchestrator("x^2 - x") == "x(x - 1)"
    assert grandOrchestrator("2*x^2 - 3x + 1") == "(x - 1)(2x - 1)"
    assert grandOrchestrator("x - x") == "0"

    try:
        grandOrchestrator("x + y")
        assert False
    except ValueError as e:
        assert "variable" in str(e)

    #* Multiply polynomial dicts
    assert multiplyPolDicts({1: 1, 0: -1}, {1: 1, 0: -2}) == {2: 1, 1: -3, 0: 2}
    assert multiplyPolDicts({0: 2}, {2: 1, 0: 1}) == {2: 2, 0: 2}
    assert multiplyPolDicts({2: 1, 0: 1}, {1: 1, 0: -1}) == {3: 1, 2: -1, 1: 1, 0: -1}
    assert multiplyPolDicts({0: 3}, {1: 1, 0: -4}) == {1: 3, 0: -12}

    #* Polynomial dictionary to string
    assert polDictToStr({2: 1, 1: -3, 0: 2}, "x") == "x^2 - 3x + 2"
    assert polDictToStr({3: 1, 2: -1, 1: 1, 0: -1}, "x") == "x^3 - x^2 + x - 1"
    assert polDictToStr({0: 5}, "x") == "5"
    assert polDictToStr({}, "x") == "0"

    #* Expand polynomial
    assert expandPolynomial("(x - 1)(x - 2)") == "x^2 - 3x + 2"
    assert expandPolynomial("2(x - 1)(x - 2)") == "2x^2 - 6x + 4"
    assert expandPolynomial("(x - 1)(x^2 + 1)") == "x^3 - x^2 + x - 1"
    assert expandPolynomial("x(x - 1)") == "x^2 - x"
    assert expandPolynomial("(2x - 1)(3x - 2)") == "6x^2 - 7x + 2"
    assert expandPolynomial("3(y - 1)(2y - 1)") == "6y^2 - 9y + 3"
    assert expandPolynomial("(2y^2 - y + 3)") == "2y^2 - y + 3"
    assert expandPolynomial("5") == "5"
    assert expandPolynomial("0") == "0"

    #* Roundtrip tests
    assert expandPolynomial(grandOrchestrator("x^2 - 3x + 2")) == "x^2 - 3x + 2"
    assert expandPolynomial(grandOrchestrator("2x^2 - 6x + 4")) == "2x^2 - 6x + 4"
    assert expandPolynomial(grandOrchestrator("6y^2 - 9y + 3")) == "6y^2 - 9y + 3"


#! Run
if __name__ == "__main__":
    test()
    keyboardLoop()