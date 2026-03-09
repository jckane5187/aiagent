import math

# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "^": lambda a, b: a ** b, # Added exponentiation operator
            "sqrt": lambda a: math.sqrt(a), # Added square root operator
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
            "^": 3, # Set precedence for exponentiation
            "sqrt": 4, # Set high precedence for square root
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_binary_operator(operators, values)
                if not operators or operators[-1] != "(":
                    raise ValueError("mismatched parentheses")
                operators.pop() # Pop '('
            elif token in self.operators:
                if token == "sqrt": # Handle unary postfix operator
                    if not values:
                        raise ValueError("not enough operands for unary operator sqrt")
                    operand = values.pop()
                    # Check for negative number under square root
                    if operand < 0:
                        raise ValueError("cannot calculate square root of a negative number")
                    values.append(self.operators[token](operand))
                else: # Handle binary operators
                    while (
                        operators
                        and operators[-1] in self.operators
                        and self.precedence.get(operators[-1], 0) >= self.precedence[token]
                        and operators[-1] != "("
                    ):
                        self._apply_binary_operator(operators, values)
                    operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            if operators[-1] == "(":
                raise ValueError("mismatched parentheses")
            self._apply_binary_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_binary_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        # This function is now specifically for binary operators.
        if len(values) < 2:
            raise ValueError(f"not enough operands for binary operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))