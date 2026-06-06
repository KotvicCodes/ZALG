#

#! Import
from fractions import Fraction


#! Input Parsing
#* Split terms
def splitTerms(polynomial: str) -> list[str]:
    """
    Input: string including polynomial

    Output: array of terms of the polynomial

    Note: returns terms in reverse order
    """

    # delete whitespace
    spaceless = polynomial.replace(" ", "")

    # add operator to the start
    if spaceless[0] not in ["+", "-"]:
        spaceless = "+" + spaceless

    # split terms
    terms = []
    currentLength = 0

    for num, char in enumerate(reversed(spaceless)):
        currentLength += 1

        if char in ["+", "-"]:
            startIndex = len(spaceless) - num
            endIndex = len(spaceless) - num + currentLength

            if char == "+":
                terms.append(spaceless[startIndex:endIndex-1])
            elif char == "-":
                terms.append(spaceless[startIndex - 1:endIndex-1])

            currentLength = 0
    return [t for t in terms if t]


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

    Output: dict, where keys are powers (int) of the variable and values are their coeficients (int)
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

        # the rest of the logic
        coef = int(term.split(f"{var}^")[0])
        power = int(term.split(f"{var}^")[1])

        if power not in powers:
            powers[power] = 0

        powers[power] += coef
    return powers


#* Parse input
def parseInput(polynomial: str) -> dict[int, int]:
    """
    Input: string including polynomial

    Output: dict, where keys are powers (int) of the variable and values are their coeficients (int)
    """

    terms = splitTerms(polynomial)
    var = getVariable(terms)
    return sumTerms(var, terms)


#! Factor Polynomial
#* Dict to array
def dictToArray(polynomialDict: dict[int, int]) -> list[int]:
    """
    Transforms the dict representation of polynomial into the array representation of it.

    Input: dict, where keys are powers (int) of the variable and values are their coeficients (int)

    Output: array of coeficients from the highest power descending to the absolute term

    Note: empty dictionary is taken as 0 polynomial
    """

    # empty dict
    if polynomialDict == {}:
        return [0]
    
    polyArray = []
    previousPower = None

    # transform dict into array with zero coef for missing powers
    for power, coef in sorted(polynomialDict.items(), reverse=True):
        if previousPower is None:
            polyArray.append(coef)
        elif previousPower - power == 1:
            polyArray.append(coef)
        else:
            for i in range(previousPower - power - 1):
                polyArray.append(0)
            polyArray.append(coef)

        previousPower = power

    # add trailing zeros
    if previousPower != 0:
        for i in range(previousPower):
                polyArray.append(0)

    return polyArray


#* Find candidate roots:
def findCandidates(polyArray: list[int]) -> list[tuple[int, int]]:
    """
    Finds all candidates for roots based on Rational root theorem

    Input: array of coeficients from the highest power descending to the absolute term

    Output: array of tupples representing fractions
    """
    candidates = []

    # delete trailing zeros
    hasZeroRoot = False
    while polyArray[-1] == 0:
        polyArray = polyArray[:-1]
        hasZeroRoot = True

    if hasZeroRoot:
        candidates.append((0, 1))


    # divisors of absolute coef
    absCoef = abs(polyArray[-1])
    absCoefDivisors = []

    for n in range(1, absCoef // 2 + 1):
        if absCoef % n == 0:
            absCoefDivisors.append(n)

    absCoefDivisors.append(absCoef)

    # divisors of leading coef
    leadCoef = abs(polyArray[0])
    leadCoefDivisors = []

    for n in range(1, leadCoef // 2 + 1):
        if leadCoef % n == 0:
            leadCoefDivisors.append(n)

    leadCoefDivisors.append(leadCoef)

    # candidates
    for lead in leadCoefDivisors:
        for ab in absCoefDivisors:
            candidates.append((ab, lead))
            candidates.append((-ab, lead))
    return candidates


#* Horner's scheme
def horner(pol: list[int], candidate: tuple[int, int]) -> bool:
    """
    Finds whether a candidate is a root of the polynomial

    Input: polynomial (array of coeficients from the highest power descending to the absolute term)
    and a single candidate depicted by a tupple (p, q) representing a fraction p/q

    Output: boolean value where True implies candidate is root and False means it's not

    Note: This function depends on fractions library
    """

    result = pol[0]
    x = Fraction(candidate[0], candidate[1])

    for coef in pol[1:]:
        result = result * x + coef

    return result == 0


#* Deflate polynomial
def deflate(pol: list[int], root: tuple[int, int]) -> list[int]:
    """
    Divides polynomial by its root using Horner's scheme

    Input: polynomial (array of coeficients from the highest power descending to the absolute term) and its root

    Output: polynomial (in array form) divided by (r - x)

    Note: This function depends on fractions library
    """

    # get coefs of deflated polynomial
    result = pol[0]
    x = Fraction(root[0], root[1])
    newPol = [result]

    for coef in pol[1:-1]:
        result = result * x + coef
        newPol.append(result)
    
    # check whether remained is zero
    result = result * x + pol[-1]

    if result != 0:
        raise ValueError("deflate() was expecting a root of a polyomial")

    # return
    return newPol


#* Get irreducible factor
def getIrreducible(polArray: list[int]) -> str:
    """
    Transforms array representing irreducible factor into a string

    Input: array of coeficients from the highest power descending to the absolute term

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
                    irreducible += f"{coefStr}x^{power}"
                elif power == 1:
                    irreducible += f"{coefStr}x"
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
def factorPolynomial(polynomialDict: dict[int, int]) -> str:
    """
    Input: dict, where keys are powers of the variable and values are coeficient before them

    Output: string of the factored polynomial
    """

    # innitialization
    polArray = dictToArray(polynomialDict)
    candidates = findCandidates(polArray)
    factoredPol = ""

    if polArray[0] != 1:
        factoredPol += str(polArray[0])

    # get roots
    roots = []

    for can in candidates:
        while horner(polArray, can):
            roots.append(can)
            polArray = deflate(polArray, can)

        if len(polArray) == 1:
            break

    # rewrite in bracket notation
    irreducible = getIrreducible(polArray)

    for root in roots:
        if root[0] == 0:
            factoredPol += "x"
        elif root[1] == 1:
            factoredPol += f"(x {signum(-root[0])} {abs(root[0])})"
        else:
            factoredPol += f"({root[1]}x {signum(-root[0])} {abs(root[0])})"

    if irreducible != "":
        factoredPol += f"({irreducible})"

    return factoredPol


#! Tests
#* Split terms
assert(splitTerms("-21x + 13") == ["13", "-21x"])
assert(splitTerms("-1") == ["-1"])
assert(splitTerms("+18 + 19 + x^5") == ["x^5", "19", "18"])
assert(splitTerms("0 + x") == ["x", "0"])
assert(splitTerms("  -21     x+  13 ") == ["13", "-21x"])
assert(splitTerms("-42") == ["-42"])
assert(splitTerms("x^2 - 3x + 1") == ["1", "-3x", "x^2"])

#* Get variable
assert(getVariable(["13", "-21x"]) == "x")
assert(getVariable(["15", "1"]) == "x")
assert(getVariable(["15", "101x^15"]) == "x")
assert(getVariable(["19x", "2x^2"]) == "x")

try:
    getVariable(["2x", "13y^2", "2"])
    assert False
except ValueError:
    assert True

#* Sum terms
assert(sumTerms("x", ["2x^2", "3x", "-5"]) == {2: 2, 1: 3, 0: -5})
assert(sumTerms("x", ["5", "3", "-2"]) == {0: 6})
assert(sumTerms("x", ["7x^3"]) == {3: 7})
assert(sumTerms("x", ["x", "x", "-x"]) == {1: 1})
assert(sumTerms("x", ["-15", "2x", "3x^12", "-x"]) == {12: 3, 1: 1, 0: -15})
assert(sumTerms("x", ["2x", "-2x"]) == {1: 0})
assert(sumTerms("x", ["3x^2", "5x^2", "-2x"]) == {2: 8, 1: -2})

#* Parse input
assert(parseInput("x^2 - 3x + 1") == {2: 1, 1: -3, 0: 1})
assert(parseInput("-x^2 + 3x - 1") == {2: -1, 1: 3, 0: -1})
assert(parseInput("5") == {0: 5})
assert(parseInput("x") == {1: 1})
assert(parseInput("-x") == {1: -1})
assert(parseInput("x - x") == {1: 0})
assert(parseInput("2y^2 - y + 3") == {2: 2, 1: -1, 0: 3})
assert(parseInput("3x + 2x - 5") == {1: 5, 0: -5})

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
assert(findCandidates([1, -3, 2]) == [(1, 1), (-1, 1), (2, 1), (-2, 1)])
assert(findCandidates([1, -5, 6]) == [(1, 1), (-1, 1), (2, 1), (-2, 1), (3, 1), (-3, 1), (6, 1), (-6, 1)])
assert(findCandidates([2, -3, 1]) == [(1, 1), (-1, 1), (1, 2), (-1, 2)])
assert(findCandidates([6, -11, 6, -1]) == [(1, 1), (-1, 1), (1, 2), (-1, 2), (1, 3), (-1, 3), (1, 6), (-1, 6)])
assert(findCandidates([1, -1, 0]) == [(0, 1), (1, 1), (-1, 1)])
assert(findCandidates([1, 0, 0, 0]) == [(0, 1), (1, 1), (-1, 1)])
assert(findCandidates([1]) == [(1, 1), (-1, 1)])
assert(findCandidates([2, 1, -6]) == [(1, 1), (-1, 1), (2, 1), (-2, 1), (3, 1), (-3, 1), (6, 1), (-6, 1), (1, 2), (-1, 2), (2, 2), (-2, 2), (3, 2), (-3, 2), (6, 2), (-6, 2)])

#* Horner's scheme
assert(horner([1, -3, 2], (1, 1)))
assert(horner([1, -3, 2], (2, 1)))
assert(not horner([1, -3, 2], (3, 1)))
assert(horner([2, -3, 1], (1, 2)))
assert(horner([1, -1, 0], (0, 1)))
assert(not horner([5], (1, 1)))

#* Deflate polynomial
assert(deflate([1, -3, 2], (1, 1)) == [1, -2])
assert(deflate([1, -3, 2], (2, 1)) == [1, -1])
assert(deflate([2, -3, 1], (1, 2)) == [2, -2])
assert(deflate([1, -6, 11, -6], (1, 1)) == [1, -5, 6])

try:
    deflate([1, -3, 2], (3, 1))
    assert False
except ValueError:
    assert True

#* Get irreducible factor
assert(getIrreducible([1, -1]) == "x - 1")
assert(getIrreducible([1, 1]) == "x + 1")
assert(getIrreducible([-1, 1]) == "-x + 1")
assert(getIrreducible([1, 0, 1]) == "x^2 + 1")
assert(getIrreducible([1, -3, 2]) == "x^2 - 3x + 2")
assert(getIrreducible([1]) == "")

#* Factor polynomial
assert(factorPolynomial({2: 1, 1: -3, 0: 2}) == "(x - 1)(x - 2)")
assert(factorPolynomial({2: 1, 1: -2, 0: 1}) == "(x - 1)(x - 1)")
assert(factorPolynomial({2: 1, 1: 3, 0: 2}) == "(x + 1)(x + 2)")
assert(factorPolynomial({2: 2, 1: -3, 0: 1}) == "2(x - 1)(2x - 1)")
assert(factorPolynomial({3: 1, 2: -1, 1: 1, 0: -1}) == "(x - 1)(x^2 + 1)")
assert(factorPolynomial({2: 1, 1: -1, 0: 0}) == "x(x - 1)")