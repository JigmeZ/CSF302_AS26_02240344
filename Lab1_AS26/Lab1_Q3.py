import math
import time

# 1 - Naive Prime Checking using Trial Division
def naive_primes_344(limit):
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, num):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# 2 - Optimized Trial Division (checking up to sqrt(n))
def optimized_primes_344(limit):
    primes = []
    for num in range(2, limit + 1):
        is_prime = True
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(num)
    return primes

# 3 - Sieve of Eratosthenes
def sieve_344(limit):
    is_prime = [True] * (limit + 1)
    is_prime[0] = False
    is_prime[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    primes = []
    for num in range(2, limit + 1):
        if is_prime[num]:
            primes.append(num)
    return primes


sizes = [10000, 50000, 100000, 500000, 1000000]

for limit in sizes:
    # 4 - Measure execution time for Naive method
    start = time.time()
    naive_primes_344(limit)
    end = time.time()
    naive_time = end - start

    # 4 - Measure execution time for Optimized Trial Division
    start = time.time()
    optimized_primes_344(limit)
    end = time.time()
    optimized_time = end - start

    # 4 - Measure execution time for Sieve of Eratosthenes
    start = time.time()
    sieve_344(limit)
    end = time.time()
    sieve_time = end - start

    print("N:", limit, "Naive:", naive_time, "Optimized:", optimized_time, "Sieve:", sieve_time)