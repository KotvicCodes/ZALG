#

#! Input Parsing
#* Split terms
def splitTerms(polynomial: str) -> list:
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
def getVariable(terms: list) -> str:
    """
    Input: array of terms of the polynomial

    Output: string of one character

    Note: currently the polynomials only support a single variable defined by a single char letter,
    and do not support parameters.
    """

    var = ""

    for term in terms:
        for char in term:
            if char.isalpha():
                if var == "":
                    var = char
                elif var != char:
                    raise ValueError("You cannot use more than one variable")

    if var == "":
        var = "x"

    return var


#* Sum terms
def sumTerms(var: str, terms: list) -> dict:
    """
    Inputs: variable of polynomial (char) & array of terms of the polynomial

    Output: dict, where keys are powers of the variable and values are coeficient before them
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
        coeficient = int(term.split(f"{var}^")[0])
        power = int(term.split(f"{var}^")[1])

        if power not in powers:
            powers[power] = 0

        powers[power] += coeficient
    return powers


#* Parse function
def parseInput(polynomial: str) -> dict:
    """
    Input: string including polynomial

    Output: dict, where keys are powers of the variable and values are coeficient before them
    """

    terms = splitTerms(polynomial)
    var = getVariable(terms)
    return sumTerms(var, terms)


#! Factor Polynomial
#* Dict to array
def dictToArray(polynomialDict: dict[int, float]) -> list[float]:
    """
    Transforms the dict representation of polynomial into the array representation of it.

    Input: dict, where keys are powers (int) of the variable and values are their coeficients (float)

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