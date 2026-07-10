# Převeď aritmetický výraz na binární strom a vypiš ho

## Identifikátory jsou velká písmena anglické abecedy A - Z
## Operátory jsou: +, -, *, /, (, )
## Optimálně vyhodnocení výrazu

# ---------

#! Node Stromu
class TreeNode:
    def __init__(self, value, leftChild=None, rightChild=None):
        self.value = value
        self.leftChild = leftChild
        self.rightChild = rightChild


#! Main
def buildTree(expression: str) -> TreeNode:
    #* Segment expression
    charArray = []

    for char in expression:
        if char != ' ':
            charArray.append(char)

    valueStack = [] # zásobník operandů a dílčích výrazů
    operatorStack = []  # zásobník operátorů a závorek


    #* Build tree
    for char in charArray:

        # identifikátor A-Z -> nový list stromu
        if char.isalpha(): # vstup pouze velká písmena A-Z
            valueStack.append(TreeNode(char))
        
        # levá závorka
        elif char == '(':
            operatorStack.append(char)
    
        # pravá závorka
        elif char == ')':
            while operatorStack[-1] != '(': # aplikuj vše až po odpovídající '('
                applyOperator(valueStack, operatorStack)
            operatorStack.pop() # došli jsme k "(" tu odstraníme

        # operátory (+ - * /)
        else:
            while (operatorStack != [] and operatorStack[-1] != '(' and getPriority(operatorStack[-1]) >= getPriority(char)):
                applyOperator(valueStack, operatorStack)
            operatorStack.append(char)

    # na konci: vyprázdnit zbylé operátory
    while operatorStack:
        applyOperator(valueStack, operatorStack)

    return valueStack[0] # kořen celého stromu


#! Helper Functions
#* Priority of operators
def getPriority(operator: str) -> int:
    if operator in ("+", "-"):
        return 1
    elif operator in ("*", "/"):
        return 2
    else: # závorka má nejmenší prioritu
        return 0
    

#* Apply operator
# sundá operátor a 2 podstromy ze zásobníků, spojí je do nového podstromu a ten vloží na valueStack
def applyOperator(valueStack: list, operatorStack: list) -> None:
    operator = operatorStack.pop()
    rightChild = valueStack.pop()
    leftChild = valueStack.pop()
    valueStack.append(TreeNode(operator, leftChild, rightChild))


#! Print Tree
#* Collect inorder
# vrátí uzly inorder (LKP) spolu s jejich hloubkou
def collectInorder(node: TreeNode | None, depth: int = 0) -> list[tuple[TreeNode, int]]:
    if node is None:
        return []
    return (collectInorder(node.leftChild, depth + 1) + [(node, depth)] + collectInorder(node.rightChild, depth + 1))


#* Print tree
def printTree(root: TreeNode) -> None:
    columnGap = 2 # mezera mezi sousedními uzly
    orderedNodes = collectInorder(root) # sloupec uzlu (= jeho index v tomto seznamu)

    # najdi rozměry "plátna"
    maxDepth = max(depth for _, depth in orderedNodes)
    width = len(orderedNodes) * columnGap

    # 2D pole mezer: pro každou úroveň jeden řádek s hodnotami a jeden pod ním pro čáry / \
    lines = [[' '] * width for _ in range(2 * maxDepth + 1)]

    for column, (node, depth) in enumerate(orderedNodes):
        # sudé řádky = hodnoty uzlů (A, *, +, ...)
        row = 2 * depth
        lines[row][column * columnGap] = str(node.value)

        # liché řádky pod hodnotami = čáry k dětem, o jeden sloupec vlevo/vpravo
        if node.leftChild is not None:
            lines[row + 1][column * columnGap - 1] = '/'
        if node.rightChild is not None:
            lines[row + 1][column * columnGap + 1] = '\\'

    # spojit znaky každého řádku do řetězce a vytisknout (bez mezer na konci)
    for line in lines:
        print(''.join(line).rstrip())


#! Extras
#* Convert tree back to expression
def treeToExpression(node: TreeNode) -> str:
    # base case
    if node.leftChild is None and node.rightChild is None:
        return str(node.value) # list -> jen písmeno, bez závorek

    # rekurzivní krok
    leftText = treeToExpression(node.leftChild)
    rightText = treeToExpression(node.rightChild)

    # vrátí vše uzávorkované - správné pořadí operací
    return f"({leftText} {node.value} {rightText})"


#! Run Script
if __name__ == "__main__":
    expression = "(A+B)*(C-D)/E+A"
    tree = buildTree(expression)
    printTree(tree)