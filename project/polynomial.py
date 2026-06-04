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


print(f"user's polynomial: {spaceless}")
print(f"terms in order: {", ".join(terms)}")