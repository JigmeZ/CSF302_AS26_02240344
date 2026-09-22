"""
Q1: Prime Number Testing
Compare Naive Method vs Optimized (sqrt) Method for checking primes.

Name: [Your Name]
Student No: 344
"""

import math
import time


# ---------------------------------------------------------
# METHOD 1: NAIVE METHOD
# Check divisibility from 2 to num-1
# ---------------------------------------------------------
def check_prime_naive(num):
    count = 0                       # how many checks we did
    if num < 2:
        return False, count

    for x in range(2, num):         # try every number from 2 to num-1
        count += 1
        if num % x == 0:
            return False, count
    return True, count


# ---------------------------------------------------------
# METHOD 2: OPTIMIZED METHOD
# Check divisibility only up to sqrt(num)
# ---------------------------------------------------------
def check_prime_fast(num):
    count = 0
    if num < 2:
        return False, count

    top = int(math.sqrt(num)) + 1
    for x in range(2, top):         # only try up to sqrt(num)
        count += 1
        if num % x == 0:
            return False, count
    return True, count


# ---------------------------------------------------------
# TEXT-BASED GRAPH (no external library needed)
# Prints a bar of '#' symbols scaled to the step count
# ---------------------------------------------------------
def print_text_graph(input_list_344, naive_count_list, fast_count_list):
    print("\n" + "=" * 70)
    print("STEP COMPARISON GRAPH (each # roughly represents 1 step)")
    print("=" * 70)

    max_steps = max(naive_count_list + fast_count_list)
    if max_steps == 0:
        max_steps = 1

    scale = 50 / max_steps          # scale bars to fit in 50 characters max

    for i in range(len(input_list_344)):
        num = input_list_344[i]
        naive_bar = "#" * int(naive_count_list[i] * scale)
        fast_bar = "#" * int(fast_count_list[i] * scale)

        print(f"\nNumber {num}:")
        print(f"  Naive     [{naive_count_list[i]:>4} steps] {naive_bar}")
        print(f"  Optimized [{fast_count_list[i]:>4} steps] {fast_bar}")

    print("\n" + "=" * 70)


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------
def main():
    input_list_344 = []             # holds the 10 numbers entered by user
    print("Enter 10 numbers to test for primality:")
    for j in range(10):
        val = int(input(f"Number {j+1}: "))
        input_list_344.append(val)

    naive_count_list = []
    fast_count_list = []
    naive_time_list = []
    fast_time_list = []

    print("\n" + "-" * 70)
    print(f"{'Number':<10}{'Prime?':<10}{'Naive Steps':<15}{'Fast Steps':<12}{'Naive Time':<12}{'Fast Time':<10}")
    print("-" * 70)

    for val in input_list_344:
        # Naive method timing
        t1 = time.perf_counter()
        is_prime_naive, steps_naive = check_prime_naive(val)
        t2 = time.perf_counter()
        time_naive = t2 - t1

        # Fast (optimized) method timing
        t1 = time.perf_counter()
        is_prime_fast, steps_fast = check_prime_fast(val)
        t2 = time.perf_counter()
        time_fast = t2 - t1

        naive_count_list.append(steps_naive)
        fast_count_list.append(steps_fast)
        naive_time_list.append(time_naive)
        fast_time_list.append(time_fast)

        print(f"{val:<10}{str(is_prime_naive):<10}{steps_naive:<15}{steps_fast:<12}"
              f"{time_naive:<12.8f}{time_fast:<10.8f}")

    # Show ASCII graph comparing steps
    print_text_graph(input_list_344, naive_count_list, fast_count_list)

    # Simple summary
    total_naive = sum(naive_count_list)
    total_fast = sum(fast_count_list)
    print(f"\nTotal steps -> Naive: {total_naive}   Optimized: {total_fast}")
    if total_fast < total_naive:
        print("Result: Optimized (sqrt) method is faster overall.")
    else:
        print("Result: Naive method is faster overall.")


if __name__ == "__main__":
    main()