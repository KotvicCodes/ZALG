#

#! Input Parsing
input = input("Input the polynomial to factorize: ")
spaceless = input.replace(" ", "")


#* Split terms
terms = []
termLenght = 0
polynomialLenght = len(spaceless)

for num, char in enumerate(spaceless):
    termLenght += 1

    if char in ["+", "-"]:
        terms.append(spaceless[(num - termLenght + 1):num])
        termLenght = 0

    if (num + 1) == polynomialLenght:
        terms.append(spaceless[(num - termLenght + 1):num + 1])

#* Discover variable 
variable = ""

for i in range(len(terms)):
    for char in terms[i]:
        if not char.isdigit():
            variable = char
            break


#* Add terms
powers = {}

for term in terms:
    # absolute & linear terms
    if "^" not in term:
        if variable in term:
            term += "^1"
        else:
            term += f"{variable}^0"

    # the rest of the logic
    print(term)
    coeficient = int(term.split(f"{variable}^")[0])
    power = int(term.split(f"{variable}^")[1])

    if power not in powers:
        powers[power] = 0

    powers[power] += coeficient


print(f"user's polynomial: {spaceless}")
print(f"terms in order: {", ".join(terms)}")
print(f"dict of terms: {powers}")