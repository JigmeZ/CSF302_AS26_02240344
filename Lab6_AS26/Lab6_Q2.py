"""
Lab 6 - Question 2: Matrix chain multiplication.
"""

import random


def matrix_chain_bottom_up(dimensions):
    """Return the minimum cost and an optimal parenthesisation."""
    matrix_count = len(dimensions) - 1
    cost = [[0] * matrix_count for _ in range(matrix_count)]
    split = [[0] * matrix_count for _ in range(matrix_count)]

    for chain_length in range(2, matrix_count + 1):
        for left in range(matrix_count - chain_length + 1):
            right = left + chain_length - 1
            cost[left][right] = float("inf")
            for middle in range(left, right):
                candidate = (
                    cost[left][middle]
                    + cost[middle + 1][right]
                    + dimensions[left]
                    * dimensions[middle + 1]
                    * dimensions[right + 1]
                )
                if candidate < cost[left][right]:
                    cost[left][right] = candidate
                    split[left][right] = middle
    return cost[0][matrix_count - 1], build_parenthesization(split, 0,
                                                               matrix_count - 1)


def build_parenthesization(split, left, right):
    if left == right:
        return f"A{left + 1}"
    middle = split[left][right]
    return "(" + build_parenthesization(split, left, middle) + build_parenthesization(
        split, middle + 1, right
    ) + ")"


def matrix_chain_brute_force(dimensions):
    """Try every parenthesisation. This is only for small chains."""
    matrix_count = len(dimensions) - 1
    if matrix_count == 1:
        return 0, "A1"

    best_cost = float("inf")
    best_order = ""
    for middle in range(1, matrix_count):
        left_cost, left_order = matrix_chain_brute_force(dimensions[: middle + 1])
        right_cost, right_order = matrix_chain_brute_force(dimensions[middle:])
        cost = (
            left_cost
            + right_cost
            + dimensions[0] * dimensions[middle] * dimensions[-1]
        )
        if cost < best_cost:
            best_cost = cost
            best_order = f"({left_order}{right_order})"
    return best_cost, best_order


def left_to_right_cost(dimensions):
    """Cost of ((A1A2)A3)... without trying other orders."""
    cost = 0
    rows = dimensions[0]
    for index in range(1, len(dimensions) - 1):
        cost += rows * dimensions[index] * dimensions[index + 1]
        rows = dimensions[index + 1]
    return cost


def verify():
    random.seed(302)
    tests = [
        [30, 35, 15, 5, 10, 20, 25],
        [5, 4, 6, 2, 7],
    ]
    for _ in range(5):
        tests.append([random.randint(2, 15) for _ in range(6)])

    print("dimensions,optimal_cost,left_to_right_cost,parenthesisation")
    for dimensions in tests:
        dynamic_cost, order = matrix_chain_bottom_up(dimensions)
        brute_cost, brute_order = matrix_chain_brute_force(dimensions)
        assert dynamic_cost == brute_cost
        print(f"{dimensions},{dynamic_cost},{left_to_right_cost(dimensions)},{order}")
        print(f"  brute-force check: {brute_cost} {brute_order}")


if __name__ == "__main__":
    verify()