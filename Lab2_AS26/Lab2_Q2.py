"""
Q2: Merge Sort Analysis (Menu-Driven Program)
Sorts an array using Merge Sort, counts comparisons (step/frequency count),
and analyzes time complexity for random, sorted, and descending-sorted data..
"""

import random
import time

arr_344 = []          # Global array used by menu options 1-4.
comparisons_344 = 0  # Global comparison counter.


# ---------------------------------------------------------
# MERGE SORT (with comparison counting)
# ---------------------------------------------------------
def merge_sort(a, ascending=True):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], ascending)
    right = merge_sort(a[mid:], ascending)
    return merge(left, right, ascending)


def merge(left, right, ascending=True):
    global comparisons_344
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        comparisons_344 += 1      # One basic operation = one comparison.
        if ascending:
            take_left = left[i] <= right[j]
        else:
            take_left = left[i] >= right[j]

        if take_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ---------------------------------------------------------
# ANY SORTING ALGORITHM FOR DESCENDING (Bubble Sort here)
# ---------------------------------------------------------
def bubble_sort_descending(a):
    global comparisons_344
    n = len(a)
    b = a.copy()
    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons_344 += 1
            if b[j] < b[j + 1]:
                b[j], b[j + 1] = b[j + 1], b[j]
    return b


# ---------------------------------------------------------
# MENU OPTIONS
# ---------------------------------------------------------
def generate_numbers():
    global arr_344
    n = int(input("Enter number of elements: "))
    arr_344 = [random.randint(1, 1000) for _ in range(n)]
    print("Generated array:", arr_344)


def display_array():
    if not arr_344:
        print("Array is empty. Generate numbers first (Option 1).")
    else:
        print("Current array:", arr_344)


def sort_ascending():
    global arr_344, comparisons_344
    if not arr_344:
        print("Array is empty. Generate numbers first.")
        return
    comparisons_344 = 0
    arr_344 = merge_sort(arr_344, ascending=True)
    print("Sorted (Ascending):", arr_344)
    print("Comparisons made:", comparisons_344)


def sort_descending():
    global arr_344, comparisons_344
    if not arr_344:
        print("Array is empty. Generate numbers first.")
        return
    comparisons_344 = 0
    arr_344 = bubble_sort_descending(arr_344)
    print("Sorted (Descending):", arr_344)
    print("Comparisons made:", comparisons_344)


def time_complexity_test(data_type):
    global comparisons_344
    n = int(input("Enter size of array (n): "))

    if data_type == "random":
        test_arr = [random.randint(1, 100000) for _ in range(n)]
    elif data_type == "sorted":
        test_arr = list(range(n))
    elif data_type == "reverse":
        test_arr = list(range(n, 0, -1))

    comparisons_344 = 0
    start = time.perf_counter()
    merge_sort(test_arr, ascending=True)
    end = time.perf_counter()

    print(f"\nData type      : {data_type}")
    print(f"n               : {n}")
    print(f"Comparisons     : {comparisons_344}")
    print(f"Time taken      : {end - start:.6f} seconds")
    print(f"Expected order  : O(n log n) -> n*log2(n) = {n * (n.bit_length()):.0f} (approx)\n")


# ---------------------------------------------------------
# MAIN MENU LOOP
# ---------------------------------------------------------
def menu():
    while True:
        print("1. Generate n random numbers -> Array")
        print("2. Display Array")
        print("3. Sort in Ascending Order (Merge Sort)")
        print("4. Sort in Descending Order (Bubble Sort)")
        print("5. Time Complexity - Ascending, Random Data")
        print("6. Time Complexity - Ascending, Already Sorted Data")
        print("7. Time Complexity - Ascending, Descending-Sorted Data")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            generate_numbers()
        elif choice == "2":
            display_array()
        elif choice == "3":
            sort_ascending()
        elif choice == "4":
            sort_descending()
        elif choice == "5":
            time_complexity_test("random")
        elif choice == "6":
            time_complexity_test("sorted")
        elif choice == "7":
            time_complexity_test("reverse")
        elif choice == "8":
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")


if __name__ == "__main__":
    menu()