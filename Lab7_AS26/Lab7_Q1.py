"""
Lab 7 - Question 1: Greedy activity selection and knapsack.

All functions are small and independent, so they can also be imported for
testing.  Run this file to see examples and random experiments.
"""

import random


def select_activities(activities, rule="finish"):
    """Return a maximum compatible set using one of three greedy rules."""
    key = {
        "finish": lambda activity: activity[1],
        "start": lambda activity: activity[0],
        "duration": lambda activity: activity[1] - activity[0],
    }[rule]
    chosen = []
    current_finish = float("-inf")
    for start, finish in sorted(activities, key=key):
        if start >= current_finish:
            chosen.append((start, finish))
            current_finish = finish
    return chosen


def find_bad_examples(trials=5000, seed=7):
    """Find examples where earliest start and shortest duration do worse."""
    random.seed(seed)
    for _ in range(trials):
        activities = []
        for _ in range(random.randint(5, 10)):
            start = random.randint(0, 15)
            activities.append((start, start + random.randint(1, 8)))
        best = len(select_activities(activities, "finish"))
        start_count = len(select_activities(activities, "start"))
        duration_count = len(select_activities(activities, "duration"))
        if start_count < best and duration_count < best:
            return activities, best, start_count, duration_count
    return None


def fractional_knapsack(items, capacity):
    """Items are (value, weight). Return value and (item, fraction) choices."""
    answer = 0.0
    choices = []
    for value, weight in sorted(items, key=lambda x: x[0] / x[1], reverse=True):
        if capacity <= 0:
            break
        fraction = min(1, capacity / weight)
        answer += value * fraction
        choices.append(((value, weight), fraction))
        capacity -= weight * fraction
    return answer, choices


def zero_one_greedy(items, capacity):
    """The tempting ratio greedy rule, but without taking fractions."""
    total = 0
    chosen = []
    for value, weight in sorted(items, key=lambda x: x[0] / x[1], reverse=True):
        if weight <= capacity:
            chosen.append((value, weight))
            total += value
            capacity -= weight
    return total, chosen


def zero_one_dp(items, capacity):
    table = [0] * (capacity + 1)
    for value, weight in items:
        for remaining in range(capacity, weight - 1, -1):
            table[remaining] = max(table[remaining],
                                   table[remaining - weight] + value)
    return table[capacity]


def worst_knapsack_ratio(trials=1000, seed=7):
    random.seed(seed)
    worst = (1.0, None)
    for _ in range(trials):
        items = [(random.randint(1, 100), random.randint(1, 30))
                 for _ in range(random.randint(4, 10))]
        capacity = random.randint(10, 50)
        greedy, _ = zero_one_greedy(items, capacity)
        optimal = zero_one_dp(items, capacity)
        ratio = greedy / optimal if optimal else 1.0
        if ratio < worst[0]:
            worst = (ratio, (items, capacity, greedy, optimal))
    return worst


def main():
    activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9),
                  (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    print("Earliest-finish selection:", select_activities(activities))
    example = find_bad_examples()
    print("\nRandom counterexample (same input for all rules):")
    print("activities:", example[0])
    print("counts: finish =", example[1], ", start =", example[2],
          ", shortest duration =", example[3])

    items = [(60, 10), (100, 20), (120, 30)]
    value, choices = fractional_knapsack(items, 50)
    print("\nFractional knapsack value:", value)
    print("fractions:", choices)

    worst = worst_knapsack_ratio()
    print("\nWorst greedy/optimal ratio found:", round(worst[0], 3))
    print("items, capacity, greedy value, optimal value:", worst[1])


if __name__ == "__main__":
    main()