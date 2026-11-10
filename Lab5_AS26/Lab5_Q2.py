"""
Lab 5 - Question 2: Counting sort and radix sort.
"""

import random
import time


def counting_sort(values, k):
    """Stable counting sort for values in the range 0..k."""
    counts = [0] * (k + 1)
    for value in values:
        counts[value] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    result = [0] * len(values)
    for value in reversed(values):  # backwards pass makes it stable
        counts[value] -= 1
        result[counts[value]] = value
    return result


def counting_sort_digit(values, divisor, base):
    counts = [0] * base
    for value in values:
        counts[(value // divisor) % base] += 1
    for i in range(1, base):
        counts[i] += counts[i - 1]
    result = [0] * len(values)
    for value in reversed(values):
        digit = (value // divisor) % base
        counts[digit] -= 1
        result[counts[digit]] = value
    return result


def radix_sort(values, base=10):
    if not values:
        return []
    result = values[:]
    divisor = 1
    largest = max(result)
    while largest // divisor > 0:
        result = counting_sort_digit(result, divisor, base)
        divisor *= base
    return result


def merge_sort(values):
    if len(values) <= 1:
        return values[:]
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]


def show_stability():
    pairs = [(2, 0), (1, 1), (2, 2), (0, 3), (1, 4), (2, 5)]
    sorted_pairs = stable_pair_counting_sort(pairs, 2)
    print("Stable pair example:")
    print("before:", pairs)
    print("after: ", sorted_pairs)


def stable_pair_counting_sort(pairs, k):
    counts = [0] * (k + 1)
    for key, _ in pairs:
        counts[key] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    result = [None] * len(pairs)
    for pair in reversed(pairs):
        key = pair[0]
        counts[key] -= 1
        result[counts[key]] = pair
    return result


def benchmark_counting():
    n = 100000
    print("\nCounting sort: n =", n)
    for k in [10, 10**3, 10**5, 10**7]:
        values = [random.randint(0, k) for _ in range(n)]
        start = time.perf_counter()
        answer = counting_sort(values, k)
        elapsed = time.perf_counter() - start
        print("k =", k, "time =", round(elapsed, 4),
              "seconds; correct =", answer == sorted(values))


def benchmark_radix():
    print("\nRadix sort and merge sort (values below 10^9)")
    for n in [10000, 100000, 500000, 1000000]:
        values = [random.randint(0, 10**9) for _ in range(n)]
        start = time.perf_counter()
        radix_sort(values, 10)
        radix10_time = time.perf_counter() - start
        start = time.perf_counter()
        radix_sort(values, 256)
        radix256_time = time.perf_counter() - start
        start = time.perf_counter()
        merge_sort(values)
        merge_time = time.perf_counter() - start
        print("n =", n, "radix base 10 =", round(radix10_time, 4),
              "radix base 256 =", round(radix256_time, 4),
              "merge sort =", round(merge_time, 4))


if __name__ == "__main__":
    show_stability()
    benchmark_counting()
    # Uncomment for the larger radix experiment:
    # benchmark_radix()