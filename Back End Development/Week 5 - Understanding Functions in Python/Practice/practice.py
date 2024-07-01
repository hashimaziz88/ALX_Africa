import random

# Generate a list of 10 random numbers between 1 and 10
random_numbers = []
for _ in range(10):
    random_numbers.append(random.randint(1, 10))
    print(random_numbers)

# Print the generated list of random numbers
print(f"Generated random numbers: {random_numbers}")

# Convert the list to a set to remove duplicates
unique_numbers = set(random_numbers)

# Convert the set back to a sorted list to display the unique numbers in order
unique_numbers_list = list(unique_numbers)
unique_numbers_list.sort()

# Print the unique numbers
print(f"Unique numbers (duplicates removed): {unique_numbers_list}")
