# [S3] Implementación de Pilas
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class Stack:
    def __init__(self):
        self.top = None
        self.count = 0 

    def push(self, element):
        new_node = Node(element)
        new_node.next = self.top
        self.top = new_node
        self.count += 1

    def pop(self):
        if self.is_empty():
            return None  
        value = self.top.value
        self.top = self.top.next
        self.count -= 1
        return value

    def peek(self):
        if self.is_empty():
            return None
        return self.top.value

    def is_empty(self):
        return self.top is None

    def size(self):
        return self.count


def is_balanced(expression):
    symbols = Stack()
    pairs = {')': '(', ']': '[', '}': '{'}

    for character in expression:
        if character in pairs.values(): 
            symbols.push(character)
        elif character in pairs: 
            if symbols.is_empty():
                return False 
            if symbols.pop() != pairs[character]:
                return False

    return symbols.is_empty() 


def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}
    stack = Stack()
    output = []

    tokens = expression.split()

    for token in tokens:
        if token.isnumeric(): 
            output.append(token)
        elif token in precedence:  # Si es operador
            while (not stack.is_empty() and stack.peek() != '(' and
                   precedence[stack.peek()] >= precedence[token]):
                output.append(stack.pop())
            stack.push(token)
        elif token == '(':  
            stack.push(token)
        elif token == ')':  
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            stack.pop() 

    while not stack.is_empty():
        output.append(stack.pop())

    return ' '.join(output)


# Pruebas
print(is_balanced("(3 + 2) * (8 / 4)"))  # True
print(is_balanced("((3 + 2) * (8 / 4)"))  # False
print(is_balanced("{[1 + 2] * (3 + 4)}"))  # True
print(is_balanced("[{(1 + 2) * 3] + 4}"))  # False

expresion = "3 + 5 * ( 2 - 8 )"
resultado = infix_to_postfix(expresion)
print(resultado) # Salida esperada: 3 5 2 8 - * +