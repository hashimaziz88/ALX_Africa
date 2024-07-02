# temp_conversion_tool.py

# Define global conversion factors
CELSIUS_TO_FAHRENHEIT_FACTOR = 9/5
FAHRENHEIT_TO_CELSIUS_FACTOR = 5/9

def convert_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius using the global conversion factor."""
    celsius = (fahrenheit - 32) * FAHRENHEIT_TO_CELSIUS_FACTOR
    return celsius


def convert_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit using the global conversion factor."""
    fahrenheit = celsius * CELSIUS_TO_FAHRENHEIT_FACTOR + 32
    return fahrenheit


def main():
    try:
        # Prompt the user to enter a temperature
        temp = float(input("Enter the temperature to convert: "))

        # Prompt the user to specify whether the temperature is in Celsius or Fahrenheit
        unit = input("Is this temperature in Celsius or Fahrenheit? (C/F): ").strip().upper()

        if unit == "C":
            # Convert from Celsius to Fahrenheit
            converted_temp = convert_to_fahrenheit(temp)
            print(f"{temp}°C is {converted_temp}°F")
        elif unit == "F":
            # Convert from Fahrenheit to Celsius
            converted_temp = convert_to_celsius(temp)
            print(f"{temp}°F is {converted_temp}°C")
        else:
            print("Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit.")
    except ValueError:
        # Handle the case where the input is not a valid number
        print("Invalid temperature. Please enter a numeric value.")


if __name__ == "__main__":
    main()
