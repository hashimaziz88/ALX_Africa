# pattern_drawing.py

# Prompt user for pattern size
pattern_size = int(input("Enter the size of the pattern: "))

# Validate input to ensure it is a positive integer
if pattern_size <= 0:
    print("Please enter a positive integer.")
else:
    # Initialize the row counter
    row = 0
    
    # Use a while loop to iterate through each row
    while row < pattern_size:
        # Use a for loop to print asterisks side by side
        for column in range(pattern_size):
            print("*", end="")
        
        # Print a newline character to move to the next row
        print()
        
        # Increment the row counter
        row += 1
