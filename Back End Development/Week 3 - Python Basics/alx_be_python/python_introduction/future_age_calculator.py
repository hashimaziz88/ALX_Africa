# Prompt user for current age
current_age = int(input("How old are you? "))

# Calculate age in 2050
future_year = 2050
current_year = 2023
years_passed = future_year - current_year
age_in_2050 = current_age + years_passed

# Print the result
print(f"In {future_year}, you will be {age_in_2050} years old.")
