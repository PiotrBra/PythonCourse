import re
import string
from itertools import combinations, product

from validExpression import valid_expression

# Compares two strings x and w character by character. Returns True if the characters at each position match
# or if w has a '-' at that position. Otherwise, returns False.
def match(x, w):
    for i in range(len(x)):
        if w[i] == '-':
            continue
        if w[i] != x[i]:
            return False
    return True

# Finds the minimum prime implicants given a set of minterms d and a term w.
def minp(d, w):
    for r in range(1, len(w) + 1):
        for c in combinations(w, r):
            new_set = set()
            for el in d:
                for pattern in c:
                    if match(el, pattern):
                        new_set.add(el)
            if len(new_set) == len(d):
                return set(c)
    return None

# Converts an infix expression expr to postfix notation using the Shunting-yard algorithm.
def onp(expr):
    output = []
    stack = []
    precedence = {'~': 4, '^': 3, '&': 2, '|': 2, '/': 2, '>': 1}

    for token in expr:
        if token.isalpha() or token in 'TF':
            output.append(token)
        elif token == '~':
            stack.append(token)
        elif token in precedence:
            while stack and precedence.get(stack[-1], 0) >= precedence[token]:
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()

    while stack:
        output.append(stack.pop())

    return ''.join(output)

# Checks if a binary operator op is balanced in the expression expr.
def bal(expr, op):
    parenthesis_count = 0  # Parenthesis counter
    for i in range(len(expr) - 1, -1, -1):
        if expr[i] == ")":
            parenthesis_count += 1
        elif expr[i] == "(":
            parenthesis_count -= 1
        elif expr[i] == op and parenthesis_count == 0:
            return i
    return None

# Checks if the expression is enclosed within brackets. If so, removes the outermost brackets.
def bracket(expr):
    if expr[0] == "(" and expr[-1] == ")" and valid_expression(expr[1:-1]):
        return bracket(expr[1:-1])
    return expr

# Replaces variables in the expression expr with their corresponding values in ver.
def map(expr, ver):
    mapping = {sorted(list(set(expr).intersection(set(string.ascii_lowercase))))[i]: ver[i] for i in range(len(ver))}
    for key in mapping:
        expr = expr.replace(key, mapping[key])
    return expr

# Generates all possible binary strings of length n.
def gen(n):
    return [''.join(seq) for seq in product('01', repeat=n)]

# Combines two binary strings s1 and s2. If the strings differ in only one position,
# replaces the differing position with '-'. If they differ in more than one position, returns None.
def combine(s1, s2):
    differing_positions = 0
    result = ""
    for i in range(len(s1)):
        if s1[i] == s2[i]:
            result += s1[i]
        else:
            result += '-'
            differing_positions += 1
    if differing_positions == 1:
        return result
    return None

# Extracts variables from the boolean expression expr.
def extract_variables(expr):
    pattern = r"[a-z]"
    variables = re.findall(pattern, expr)
    unique_variables = sorted(set(variables))
    return unique_variables

# Evaluates a boolean expression given in postfix notation using a stack-based approach.
def val(expr):
    stack = []
    for token in expr:
        if token in '01':
            stack.append(int(token))
        elif token == 'T':
            stack.append(1)
        elif token == 'F':
            stack.append(0)
        elif token == '|':
            b = stack.pop()
            a = stack.pop()
            stack.append(a | b)
        elif token == '&':
            b = stack.pop()
            a = stack.pop()
            stack.append(a & b)
        elif token == '>':
            b = stack.pop()
            a = stack.pop()
            stack.append((not a) | b)
        elif token == '^':
            b = stack.pop()
            a = stack.pop()
            stack.append(a ^ b)
        elif token == '~':
            a = stack.pop()
            stack.append(not a)
        elif token == '/':
            b = stack.pop()
            a = stack.pop()
            stack.append(not (a and b))
        else:
            raise ValueError(f"Unknown operator: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid RPN expression - unexpected number of elements on the stack")

    return int(stack.pop())
