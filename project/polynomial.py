#

#! Input Parsing
input = input("Input the polynomial to factorize: ")
spaceless = input.replace(" ", "")

# add operator to the start
if spaceless[0] != "-":
    spaceless = "+" + spaceless


#* Split terms
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


#* Discover variable 
variable = ""

for i in range(len(terms)):
    for char in terms[i]:
        if not char.isdigit():
            variable = char
            break

print(f"terms in order: {", ".join(terms)}")


#* Add terms
powers = {}

for term in terms:
    # absolute & linear terms
    if "^" not in term:
        if variable in term:
            term += "^1"
        else:
            term += f"{variable}^0"
    
    # add leading 1s
    if term[0] == variable:
        term = "1" + term
        print(f"term leading 1: {term}")
    elif term.startswith(f"-{variable}"):
        term = "-1" + term[1:]
        print(f"term leading 2: {term}")

    # the rest of the logic
    print(term)
    coeficient = int(term.split(f"{variable}^")[0])
    power = int(term.split(f"{variable}^")[1])

    if power not in powers:
        powers[power] = 0

    powers[power] += coeficient


print(f"dict of terms: {powers}")