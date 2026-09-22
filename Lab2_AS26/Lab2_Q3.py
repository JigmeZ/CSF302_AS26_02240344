# This program multiplies two square matrices.
# The matrix size must be a power of 2, such as 2, 4, or 8.
"""
Q3: Square Matrix Multiplication
Multiply two n x n matrices where n is a power of 2.
"""

import random  # Used to generate random matrix values.


def print_matrix(matrix):
	# Visit each row in the matrix.
	for row in matrix:
		# Print every value in the current row with equal spacing.
		print(" ".join(f"{value:4}" for value in row))


def multiply_matrices(matrix_a, matrix_b):
	# Get the number of rows and columns in the square matrices.
	size = len(matrix_a)
	# Create a result matrix filled with zeroes.
	result = [[0 for _ in range(size)] for _ in range(size)]
	# Store the number of multiplication operations.
	multiplication_count = 0
	# Store the number of addition operations.
	addition_count = 0

	# Select a row from matrix A.
	for row in range(size):
		# Select a column from matrix B.
		for column in range(size):
			# Select matching values from the row and column.
			for index in range(size):
				# Multiply the matching values and add them to the result cell.
				result[row][column] += matrix_a[row][index] * matrix_b[index][column]
				# Count one multiplication for this loop iteration.
				multiplication_count += 1
				# The first product starts the sum; later products require addition.
				if index > 0:
					# Count one addition after the first product.
					addition_count += 1

	# Return the answer and both operation counts.
	return result, multiplication_count, addition_count


def is_power_of_two(number):
	# A power of 2 has only one 1 in its binary representation.
	return number > 0 and (number & (number - 1)) == 0


def main():
	# Ask the user for the matrix size and convert the input to an integer.
	size = int(input("Enter matrix size (2, 4, 8, ...): "))

	# Reject sizes that are not positive powers of 2.
	if not is_power_of_two(size):
		# Explain the valid input requirement.
		print("Size must be a positive power of 2.")
		# Stop the program when the size is invalid.
		return

	# Create the first random matrix using values from 1 to 9.
	matrix_a_344 = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]
	# Create the second random matrix using values from 1 to 9.
	matrix_b_344 = [[random.randint(1, 9) for _ in range(size)] for _ in range(size)]

	# Multiply the matrices and receive the operation counts.
	result_344, multiplication_count, addition_count = multiply_matrices(
		matrix_a_344, matrix_b_344
	)

	# Display the first input matrix.
	print("\nMatrix A:")
	print_matrix(matrix_a_344)
	# Display the second input matrix.
	print("\nMatrix B:")
	print_matrix(matrix_b_344)
	# Display the multiplication result.
	print("\nResult matrix:")
	print_matrix(result_344)

	# Add both operation types to get the total step count.
	total_steps = multiplication_count + addition_count
	# Display the operation frequency counts.
	print("\nOperation counts:")
	print(f"Multiplications: {multiplication_count}")
	print(f"Additions:       {addition_count}")
	
	print(f"Total steps:     {total_steps}")


# Analysis: Standard matrix multiplication performs n^3 multiplications and
# n^2(n - 1) additions, so its time complexity is O(n^3).
if __name__ == "__main__":
	# Run main only when this file is executed directly.
	main()
