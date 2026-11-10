"""
Lab 7 - Question 4: randomized algorithms.
"""

import random
import time


def quickselect(values, k):
    """Return the zero-based k-th smallest value without fully sorting."""
    values = values[:]
    low, high = 0, len(values) - 1
    while low <= high:
        pivot = values[random.randint(low, high)]
        smaller = [x for x in values[low:high + 1] if x < pivot]
        equal = [x for x in values[low:high + 1] if x == pivot]
        if k < low + len(smaller):
            values[low:low + len(smaller)] = smaller
            high = low + len(smaller) - 1
        elif k < low + len(smaller) + len(equal):
            return pivot
        else:
            start = low + len(smaller) + len(equal)
            values[start:high + 1] = [
                x for x in values[low:high + 1] if x > pivot
            ]
            low = start
    raise IndexError("k is outside the list")


def is_prime_trial(n):
    if n < 2:
        return False
    divisor = 2
    while divisor * divisor <= n:
        if n % divisor == 0:
            return False
        divisor += 1
    return True


def miller_rabin(n, rounds=5):
    if n in (2, 3):
        return True
    if n < 2 or n % 2 == 0:
        return False
    power, odd_part = 0, n - 1
    while odd_part % 2 == 0:
        power += 1
        odd_part //= 2
    for _ in range(rounds):
        base = random.randrange(2, n - 1)
        value = pow(base, odd_part, n)
        if value in (1, n - 1):
            continue
        for _ in range(power - 1):
            value = (value * value) % n
            if value == n - 1:
                break
        else:
            return False
    return True


def main():
    values = [random.randint(0, 10**6) for _ in range(10000)]
    k = 5000
    start = time.perf_counter()
    selected = quickselect(values, k)
    quick_time = time.perf_counter() - start
    start = time.perf_counter()
    sorted_value = sorted(values)[k]
    sort_time = time.perf_counter() - start
    print("Quickselect correct:", selected == sorted_value)
    print("n = 10000: quickselect =", round(quick_time, 5),
          "s, sorting =", round(sort_time, 5), "s")

    print("\nMiller-Rabin versus trial division (20 random 12-digit numbers):")
    agree = 0
    for _ in range(20):
        number = random.randint(10**11, 10**12 - 1)
        trial = is_prime_trial(number)
        rabin = miller_rabin(number, 8)
        agree += trial == rabin
    print("agreeing results:", agree, "/ 20")

    false_primes = sum(miller_rabin(561, 1) for _ in range(1000))
    print("\nWith one Miller-Rabin round, 561 was called prime",
          false_primes, "times out of 1000.")


if __name__ == "__main__":
    main()