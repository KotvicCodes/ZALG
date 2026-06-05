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
    if spaceless[0] != "-":
        spaceless = "+" + spaceless

    # split terms
    terms = []
    currentLength = 0

    for num, char in enumerate(reversed(spaceless)):
        currentLength += 1
        print(char, num)

        if char in ["+", "-"]:
            startIndex = len(spaceless) - num
            endIndex = len(spaceless) - num + currentLength

            if char == "+":
                terms.append(spaceless[startIndex:endIndex-1])
                print(spaceless[startIndex:endIndex-1])
            elif char == "-":
                terms.append(spaceless[startIndex - 1:endIndex-1])
                print(spaceless[startIndex - 1:endIndex-1])

            currentLength = 0
    return terms


#* Get variable
def getVariable(terms: list) -> str:
    """
    Input: array of terms of the polynomial

    Output: string of one character
    """

    var = ""

    for i in range(len(terms)):
        for char in terms[i]:
            if not char.isdigit():
                var = char
                break

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
            print(f"term leading 1: {term}")
        elif term.startswith(f"-{var}"):
            term = "-1" + term[1:]
            print(f"term leading 2: {term}")

        # the rest of the logic
        print(term)
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