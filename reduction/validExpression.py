def valid_expression(expr):
    # Define sets of variables and operators
    variables = set('abcdefghijklmnopqrstuvwxyz') | set('TF')
    operators = set('~^&|/>')

    # Flag indicating whether we expect an operand
    expecting_operand = True

    # Counter for parentheses
    parentheses_count = 0

    for char in expr:
        if expecting_operand:
            # If we expect an operand
            if char in variables:
                expecting_operand = False  # After a variable/constant, we expect an operator
            elif char == '(':
                parentheses_count += 1
            elif char == '~':  # Negation is a unary operator and we still expect an operand
                continue
            else:
                return False  # Unexpected character
        else:
            # If we expect an operator
            if char in operators - set('~'):  # Negation cannot occur as a binary operator
                expecting_operand = True  # After a binary operator, we expect an operand
            elif char == ')':
                # If a closing parenthesis is encountered
                if parentheses_count == 0:
                    return False  # Closing parenthesis without opening
                parentheses_count -= 1
                expecting_operand = False  # After closing parenthesis, we expect an operator
            else:
                return False  # Unexpected character

    # Check if the last element was an operand and parentheses were correctly paired
    return not expecting_operand and parentheses_count == 0
