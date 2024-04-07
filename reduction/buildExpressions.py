# Function to build an expression from minimal vectors
def build_expression_from_vectors(vectors, variables):
    expressions = []
    patterns = {
        ('01', '10'): lambda variables: f"{variables[0]}^{variables[1]}",
        ('-1', '0-'): lambda variables: f"{variables[0]}>{variables[1]}",
        ('-0', '0-'): lambda variables: f"{variables[0]}/{variables[1]}",
        ('001', '010', '100', '111'): lambda variables: f"{variables[0]}^{variables[1]}^{variables[2]}",
        ('--1', '10-'): lambda variables: f"{variables[0]}>{variables[1]}>{variables[2]}",
        ('--0', '11-'): lambda variables: f"{variables[0]}/{variables[1]}/{variables[2]}"
    }

    def detect_pattern(vectors, variables):
        sorted_vectors = tuple(sorted(vectors))
        # Check if the sorted vectors match any pattern
        if sorted_vectors in patterns:
            # Execute the function associated with the pattern
            return patterns[sorted_vectors](variables)
        return None

    pattern = detect_pattern(vectors, variables)

    if pattern:
        return pattern

    for vector in vectors:
        expression_parts = []

        for i, value in enumerate(vector):
            if value == '1':
                expression_parts.append(f"{variables[i]}")
            elif value == '0':
                expression_parts.append(f"~{variables[i]}")

        if len(expression_parts) > 1:
            expression_part = f"({'&'.join(expression_parts)})"
        else:
            expression_part = '&'.join(expression_parts)

        if expression_part:
            expressions.append(expression_part)

    final_expression = "|".join(expressions)
    return final_expression
