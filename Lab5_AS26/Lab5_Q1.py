"""
Lab 5 - Question 1: Quicksort variants

Run this file to print a comparison table.  The comparison counter counts
comparisons between array values (not index calculations).
"""

import random
import time


def lomuto_partition(a, low, high, count):
    pivot = a[high]
    i = low
    for j in range(low, high):
        count[0] += 1
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[high] = a[high], a[i]
    return i


def quicksort_lomuto(a):
    count = [0]
    low, high = 0, len(a) - 1
    while low < high:
        p = lomuto_partition(a, low, high, count)
        # Recurse only into the smaller side.
        if p - low < high - p:
            quicksort_lomuto_part(a, low, p - 1, count)
            low = p + 1
        else:
            quicksort_lomuto_part(a, p + 1, high, count)
            high = p - 1
    return count[0]


def quicksort_lomuto_part(a, low, high, count):
    while low < high:
        p = lomuto_partition(a, low, high, count)
        if p - low < high - p:
            quicksort_lomuto_part(a, low, p - 1, count)
            low = p + 1
        else:
            quicksort_lomuto_part(a, p + 1, high, count)
            high = p - 1


def hoare_partition(a, low, high, count):
    pivot = a[(low + high) // 2]
    i, j = low - 1, high + 1
    while True:
        i += 1
        while a[i] < pivot:
            count[0] += 1
            i += 1
        count[0] += 1
        j -= 1
        while a[j] > pivot:
            count[0] += 1
            j -= 1
        count[0] += 1
        if i >= j:
            return j
        a[i], a[j] = a[j], a[i]


def quicksort_hoare(a):
    count = [0]
    quicksort_hoare_part(a, 0, len(a) - 1, count)
    return count[0]


def quicksort_hoare_part(a, low, high, count):
    while low < high:
        split = hoare_partition(a, low, high, count)
        if split - low < high - split:
            quicksort_hoare_part(a, low, split, count)
            low = split + 1
        else:
            quicksort_hoare_part(a, split + 1, high, count)
            high = split


def quicksort_random(a):
    count = [0]
    quicksort_random_part(a, 0, len(a) - 1, count)
    return count[0]


def quicksort_random_part(a, low, high, count):
    while low < high:
        pivot_index = random.randint(low, high)
        a[pivot_index], a[high] = a[high], a[pivot_index]
        p = lomuto_partition(a, low, high, count)
        if p - low < high - p:
            quicksort_random_part(a, low, p - 1, count)
            low = p + 1
        else:
            quicksort_random_part(a, p + 1, high, count)
            high = p - 1


def quicksort_three_way(a):
    count = [0]
    quicksort_three_way_part(a, 0, len(a) - 1, count)
    return count[0]


def quicksort_three_way_part(a, low, high, count):
    while low < high:
        pivot = a[low]
        lt, i, gt = low, low + 1, high
        while i <= gt:
            count[0] += 1
            if a[i] < pivot:
                a[lt], a[i] = a[i], a[lt]
                lt += 1
                i += 1
            elif a[i] > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
        if lt - low < high - gt:
            quicksort_three_way_part(a, low, lt - 1, count)
            low = gt + 1
        else:
            quicksort_three_way_part(a, gt + 1, high, count)
            high = lt - 1


def make_inputs(n):
    return {
        "random": [random.randint(0, n) for _ in range(n)],
        "sorted": list(range(n)),
        "reverse": list(range(n, 0, -1)),
        "duplicates": [random.randint(0, 9) for _ in range(n)],
    }


def run():
    algorithms = [
        ("Lomuto", quicksort_lomuto),
        ("Hoare", quicksort_hoare),
        ("Randomised", quicksort_random),
        ("Three-way", quicksort_three_way),
    ]
    sizes = [1000, 2000, 4000, 8000, 16000]
    print("Input,Size,Algorithm,Comparisons,Time (seconds)")
    for n in sizes:
        for input_name, original in make_inputs(n).items():
            for algorithm_name, algorithm in algorithms:
                data = original[:]
                start = time.perf_counter()
                comparisons = algorithm(data)
                elapsed = time.perf_counter() - start
                assert data == sorted(original)
                print(input_name, n, algorithm_name, comparisons,
                      f"{elapsed:.6f}", sep=",")


if __name__ == "__main__":
    run()