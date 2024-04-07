from buildExpressions import build_expression_from_vectors
from utils import *
from validExpression import valid_expression


# Function to reduce a boolean expression to its minimal form
def reduce_expression(expr):
    # Generate truth vectors from the expression
    truth_vectors = generate_truth_vectors(bracket(expr))

    # Return 'F' if truth vectors are empty (expression always evaluates to false)
    if not truth_vectors:
        return 'F'

    # Set of all possible vectors for the given expression length
    all_possible_vectors = {''.join(seq) for seq in product('01', repeat=len(truth_vectors[0]))}

    # Return 'T' if truth vectors cover all possibilities (expression always evaluates to true)
    if set(truth_vectors) == all_possible_vectors:
        return 'T'

    # Reduce truth vectors
    minimal_vectors = minp(truth_vectors, reduce(truth_vectors))

    # Return 'F' if there are no minimal vectors (no satisfying values)
    if not minimal_vectors:
        return 'F'

    # Return original expression if reduction doesn't change vectors
    if minimal_vectors == truth_vectors:
        return expr

    # Extract variables from the expression
    variables = extract_variables(expr)

    # Build reduced expression from minimal vectors
    reduced_expr = build_expression_from_vectors(minimal_vectors, variables)

    # Return original expression if reduced expression has the same length
    if len(reduced_expr) == len(expr):
        return expr

    # Return reduced expression without unnecessary brackets
    return bracket(reduced_expr)


# Function to remove unnecessary brackets from an expression
def bracket(expr):
    if expr[0] == "(" and expr[-1] == ")" and valid_expression(expr[1:-1]):
        return bracket(expr[1:-1])
    return expr


# Function to generate all truth vectors for a given expression
def generate_truth_vectors(expr):
    variables = sorted(set(filter(str.isalpha, expr)) - {'T', 'F'})
    onp_expr = onp(bracket(expr))

    all_value_vectors = gen(len(variables))

    truth_vectors = []

    for value_vector in all_value_vectors:
        mapped_onp_expr = map(onp_expr, value_vector)
        if val(mapped_onp_expr) == 1:
            truth_vectors.append(value_vector)

    return truth_vectors


# Function to reduce a set of vectors to their minimal form
def reduce(s):
    while True:
        s2 = set()
        changed = False
        for e1 in s:
            for e2 in s:
                if e1 != e2:
                    n = combine(e1, e2)
                    if n:
                        changed = True
                        s2.add(n)
        s2.update(e1 for e1 in s if all(combine(e1, e2) is None for e2 in s if e1 != e2))
        if not changed:
            break
        s = s2
    return s
