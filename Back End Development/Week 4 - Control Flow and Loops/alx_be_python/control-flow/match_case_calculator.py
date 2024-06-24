# match_case_calculator.py

# Prompt the user to enter two numbers
first_number = float(input("Enter the first number: "))
second_number = float(input("Enter the second number: "))

# Prompt the user to choose an operation
operation = input("Choose the operation (+, -, *, /): ").strip()

# Perform the calculation using a match case statement
match operation:
    case '+':
        result = first_number + second_number
        print(f"The result is {result}.")
    case '-':
        result = first_number - second_number
        print(f"The result is {result}.")
    case '*':
        result = first_number * second_number
        print(f"The result is {result}.")
    case '/':
        if second_number != 0:
            result = first_number / second_number
            print(f"The result is {result}.")
        else:
            print("Cannot divide by zero.")
    case _:
        print("Invalid operation. Please choose from +, -, *, /.")
