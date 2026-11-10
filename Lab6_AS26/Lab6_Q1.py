"""
Lab 6 - Question 1: Rod cutting.

The three solutions all return the best revenue and the cuts that produce it.
The timing experiment also counts calls to the main solution function.
"""

import time


PRICES = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def naive_cut(prices, n, calls=None):
    """Solve rod cutting by trying every first cut."""
    if calls is not None:
        calls[0] += 1
    if n == 0:
        return 0, []

    best_revenue = -1
    best_cuts = []
    for first_cut in range(1, n + 1):
        revenue, cuts = naive_cut(prices, n - first_cut, calls)
        revenue += prices[first_cut]
        if revenue > best_revenue:
            best_revenue = revenue
            best_cuts = [first_cut] + cuts
    return best_revenue, best_cuts


def memoized_cut(prices, n, calls=None, memo=None):
    """Solve rod cutting top-down, saving answers already calculated."""
    if calls is not None:
        calls[0] += 1
    if memo is None:
        memo = {0: (0, [])}
    if n in memo:
        return memo[n]

    best_revenue = -1
    best_cuts = []
    for first_cut in range(1, n + 1):
        revenue, cuts = memoized_cut(prices, n - first_cut, calls, memo)
        revenue += prices[first_cut]
        if revenue > best_revenue:
            best_revenue = revenue
            best_cuts = [first_cut] + cuts
    memo[n] = (best_revenue, best_cuts)
    return memo[n]


def bottom_up_cut(prices, n, calls=None):
    """Solve rod cutting bottom-up using a table."""
    revenue = [0] * (n + 1)
    cuts = [[] for _ in range(n + 1)]
    for length in range(1, n + 1):
        if calls is not None:
            calls[0] += 1
        for first_cut in range(1, length + 1):
            candidate = prices[first_cut] + revenue[length - first_cut]
            if candidate > revenue[length]:
                revenue[length] = candidate
                cuts[length] = [first_cut] + cuts[length - first_cut]
    return revenue[n], cuts[n]


def prices_up_to(length):
    """Use the given table, then p[i] = 3*i for longer rods."""
    prices = PRICES[:]
    for size in range(len(prices), length + 1):
        prices.append(3 * size)
    return prices


def benchmark():
    print("\nComparison for longer rods")
    print("n,version,calls,time_seconds")
    for n in [5, 10, 15, 20, 25]:
        prices = prices_up_to(n)
        for name, solver in [
            ("naive", naive_cut),
            ("memoized", memoized_cut),
            ("bottom_up", bottom_up_cut),
        ]:
            calls = [0]
            start = time.perf_counter()
            solver(prices, n, calls)
            elapsed = time.perf_counter() - start
            print(f"{n},{name},{calls[0]},{elapsed:.6f}")

    print("\nExplanation: naive recursion repeats the same subproblems, so its")
    print("calls grow exponentially. Memoization calculates each length once.")
    print("Bottom-up also calculates each length once and avoids recursion.")


def main():
    print("Best revenue and cuts")
    for n in range(1, 11):
        revenue, cuts = bottom_up_cut(PRICES, n)
        print(f"n={n:2d}: revenue={revenue:2d}, cuts={cuts}")
    benchmark()


if __name__ == "__main__":
    main()