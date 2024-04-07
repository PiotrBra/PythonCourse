from reduction import reduce_expression
from validExpression import valid_expression
def main():
    try:
        print("podaj wyrazenie logiczne")
        expression = input().replace(" ", "")
        if not valid_expression(expression):
            return 'ERROR'

        reduced_expression = reduce_expression(expression)
        return reduced_expression

    except Exception as e:
        return 'ERROR'

if __name__ == "__main__":
    result = main()
    print(result)