"""
Lab 5 - Question 3: Counting inversions and Kendall tau distance.
"""

import random
import time


def brute_force_inversions(values):
    total = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] > values[j]:
                total += 1
    return total


def merge_count(left, right):
    result = []
    i = j = inversions = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            inversions += len(left) - i
            j += 1
    return result + left[i:] + right[j:], inversions


def merge_sort_inversions(values):
    if len(values) <= 1:
        return values[:], 0
    middle = len(values) // 2
    left, left_count = merge_sort_inversions(values[:middle])
    right, right_count = merge_sort_inversions(values[middle:])
    merged, split_count = merge_count(left, right)
    return merged, left_count + right_count + split_count


def verify_answers():
    # Checking every n from 1 to 2000 would itself take unnecessarily long.
    # These representative sizes still test the required range.
    for n in [1, 10, 100, 500, 1000, 2000]:
        values = [random.randint(0, n) for _ in range(n)]
        brute = brute_force_inversions(values)
        fast = merge_sort_inversions(values)[1]
        if brute != fast:
            return False, n
    return True, 2000


def benchmark():
    print("Inversion count timings")
    for n in [1000, 10000, 100000, 1000000]:
        values = [random.randint(0, n) for _ in range(n)]
        start = time.perf_counter()
        merge_sort_inversions(values)
        fast_time = time.perf_counter() - start
        print("n =", n, "merge sort =", round(fast_time, 4), "seconds")

        if n <= 2000:
            start = time.perf_counter()
            brute_force_inversions(values)
            brute_time = time.perf_counter() - start
            print("       brute force =", round(brute_time, 4), "seconds")
        else:
            print("       brute force = skipped (would be too slow)")


def kendall_tau():
    print("\nEnter the same 10 movie names in each user's ranking.")
    first = input("User 1 ranking (comma separated): ").split(",")
    second = input("User 2 ranking (comma separated): ").split(",")
    first = [movie.strip() for movie in first]
    second = [movie.strip() for movie in second]
    if len(first) != 10 or len(second) != 10 or set(first) != set(second):
        print("Please enter exactly the same 10 movie names, once per ranking.")
        return
    position = {movie: i for i, movie in enumerate(second)}
    converted = [position[movie] for movie in first]
    distance = merge_sort_inversions(converted)[1]
    print("Kendall tau distance:", distance)
    print("Maximum possible distance for 10 movies:", 45)


if __name__ == "__main__":
    correct, checked = verify_answers()
    print("Verification passed:", correct, "(random arrays up to n =", checked, ")")
    benchmark()
    # Uncomment when you want to enter the movie rankings:
    # kendall_tau()