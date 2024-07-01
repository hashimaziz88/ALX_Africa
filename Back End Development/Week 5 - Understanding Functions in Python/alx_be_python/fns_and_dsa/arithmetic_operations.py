# arithmetic_operations.py

def perform_operation(num1, num2, operation):
    """
    Perform arithmetic operations based on operation parameter.

    Parameters:
    num1 (float): First number
    num2 (float): Second number
    operation (str): Operation to perform ('add', 'subtract', 'multiply', 'divide')

    Returns:
    float: Result of the arithmetic operation
    """
    if operation == 'add':
        return num1 + num2
    elif operation == 'subtract':
        return num1 - num2
    elif operation == 'multiply':
        return num1 * num2
    elif operation == 'divide':
        # Check for division by zero
        if num2 == 0:
            return "Error: Division by zero is undefined"
        else:
            return num1 / num2
    else:
        return "Error: Invalid operation"
