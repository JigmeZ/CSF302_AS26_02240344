import random


# Generate sorted random array
def generate_array(n):
    array = random.sample(range(1, n * 10), n)
    array.sort()
    return array


# Binary Search
def binary_search(array, key):
    left = 0
    right = len(array) - 1
    comparisons = 0

    while left <= right:

        mid = (left + right) // 2

        comparisons += 1

        if array[mid] == key:
            return mid, comparisons

        if key < array[mid]:
            right = mid - 1
        else:
            left = mid + 1

    return -1, comparisons


# Ternary Search
def ternary_search(array, key):
    left = 0
    right = len(array) - 1
    comparisons = 0

    while left <= right:

        third = (right - left) // 3

        mid1 = left + third
        mid2 = right - third

        comparisons += 1

        if array[mid1] == key:
            return mid1, comparisons

        comparisons += 1

        if array[mid2] == key:
            return mid2, comparisons

        if key < array[mid1]:
            right = mid1 - 1

        elif key > array[mid2]:
            left = mid2 + 1

        else:
            left = mid1 + 1
            right = mid2 - 1

    return -1, comparisons


# Main program
array = []

while True:

    print("\n===== MENU =====")
    print("1. Generate sorted random array")
    print("2. Display array")
    print("3. Binary Search")
    print("4. Ternary Search")
    print("5. Best case comparison")
    print("6. Worst case comparison")
    print("7. Comparison table")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    # Generate array
    if choice == 1:

        n = int(input("Enter n: "))

        array = generate_array(n)

        print("Array generated successfully.")

    # Display array
    elif choice == 2:

        if len(array) == 0:
            print("Generate the array first.")
        else:
            print(array)

    # Binary Search
    elif choice == 3:

        if len(array) == 0:
            print("Generate the array first.")
        else:

            key = int(input("Enter key: "))

            position, comparisons = binary_search(array, key)

            if position != -1:
                print("Key found at index:", position)
            else:
                print("Key not found.")

            print("Comparisons:", comparisons)

    # Ternary Search
    elif choice == 4:

        if len(array) == 0:
            print("Generate the array first.")
        else:

            key = int(input("Enter key: "))

            position, comparisons = ternary_search(array, key)

            if position != -1:
                print("Key found at index:", position)
            else:
                print("Key not found.")

            print("Comparisons:", comparisons)

    # Best case
    elif choice == 5:

        if len(array) == 0:
            print("Generate the array first.")
        else:

            key = array[len(array) // 2]

            _, binary_count = binary_search(array, key)
            _, ternary_count = ternary_search(array, key)

            print("\nBest Case")
            print("Binary Search:", binary_count)
            print("Ternary Search:", ternary_count)

    # Worst case
    elif choice == 6:

        if len(array) == 0:
            print("Generate the array first.")
        else:

            key = -1

            _, binary_count = binary_search(array, key)
            _, ternary_count = ternary_search(array, key)

            print("\nWorst Case")
            print("Binary Search:", binary_count)
            print("Ternary Search:", ternary_count)

    # Comparison table
    elif choice == 7:

        print("\n n\tBinary\tTernary")

        for n in [10, 20, 50, 100, 200, 500, 1000]:

            array = generate_array(n)

            key = -1

            _, binary_count = binary_search(array, key)
            _, ternary_count = ternary_search(array, key)

            print(n, "\t", binary_count, "\t", ternary_count)

    # Exit
    elif choice == 8:

        print("Program ended.")
        break

    else:
        print("Invalid choice.")


#--------------------------------------------------
#--Analysis--
#Binary Search divides the search space into two parts, while Ternary Search divides it into three parts. 
#Both have O(log n) time complexity. 
#Binary Search generally performs fewer comparisons per step, while Ternary Search uses more comparison points at each step. 
#The experiment compares their actual number of comparisons for different values of n.

# --Conclusion--
#Both algorithms are efficient for sorted arrays, and the experiment shows how their number of comparisons changes as the input size increases.
#------------------------------------------------