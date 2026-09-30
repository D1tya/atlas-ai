from langchain_core.tools import tool


@tool
def calculator(
    a: float,
    b: float,
    operation: str,
) -> float:
    """Perform arithmetic using two numbers.

    Supported operations:
    add, subtract, multiply, divide.
    """

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        if b == 0:
            raise ValueError(
                "Cannot divide by zero."
            )

        return a / b

    raise ValueError(
        f"Unsupported operation: {operation}"
    )