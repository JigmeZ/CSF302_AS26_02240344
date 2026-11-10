"""Modular matrix exponentiation exercises.

All matrices are represented as lists of lists.  The functions in this file
do not mutate their inputs, and every result is reduced modulo ``modulus``.
"""

from __future__ import annotations

import random
import time
from typing import Sequence


Matrix = list[list[int]]


def _validate_modulus(modulus: int) -> None:
    if modulus <= 0:
        raise ValueError("The modulus must be a positive integer.")


def _validate_exponent(exponent: int) -> None:
    if exponent < 0:
        raise ValueError("The exponent cannot be negative.")


def _validate_square_matrix(matrix: Sequence[Sequence[int]]) -> int:
    """Return the dimension of a non-empty square matrix."""
    dimension = len(matrix)
    if dimension == 0:
        raise ValueError("The matrix must not be empty.")
    if any(len(row) != dimension for row in matrix):
        raise ValueError("The matrix must be square.")
    return dimension


def multiply_matrices(
    left: Sequence[Sequence[int]],
    right: Sequence[Sequence[int]],
    modulus: int,
) -> Matrix:
    """Multiply two square matrices and reduce each element modulo ``modulus``."""
    _validate_modulus(modulus)
    left_dimension = _validate_square_matrix(left)
    right_dimension = _validate_square_matrix(right)
    if left_dimension != right_dimension:
        raise ValueError("Both matrices must have the same dimension.")

    return [
        [
            sum(left[row][inner] * right[inner][column]
                for inner in range(left_dimension)) % modulus
            for column in range(left_dimension)
        ]
        for row in range(left_dimension)
    ]


def identity_matrix(dimension: int) -> Matrix:
    """Return the identity matrix of the requested dimension."""
    if dimension <= 0:
        raise ValueError("The dimension must be a positive integer.")
    return [
        [1 if row == column else 0 for column in range(dimension)]
        for row in range(dimension)
    ]


def _reduced_matrix(matrix: Sequence[Sequence[int]], modulus: int) -> Matrix:
    dimension = _validate_square_matrix(matrix)
    return [[value % modulus for value in matrix[row]] for row in range(dimension)]


def naive_matrix_power(
    matrix: Sequence[Sequence[int]],
    exponent: int,
    modulus: int,
) -> Matrix:
    """Calculate ``matrix**exponent mod modulus`` by repeated multiplication."""
    _validate_modulus(modulus)
    _validate_exponent(exponent)
    dimension = _validate_square_matrix(matrix)
    result = identity_matrix(dimension)
    base = _reduced_matrix(matrix, modulus)

    for _ in range(exponent):
        result = multiply_matrices(result, base, modulus)
    return result


def binary_matrix_power(
    matrix: Sequence[Sequence[int]],
    exponent: int,
    modulus: int,
) -> Matrix:
    """Calculate ``matrix**exponent mod modulus`` using repeated squaring."""
    _validate_modulus(modulus)
    _validate_exponent(exponent)
    dimension = _validate_square_matrix(matrix)
    result = identity_matrix(dimension)
    base = _reduced_matrix(matrix, modulus)

    while exponent:
        if exponent & 1:
            result = multiply_matrices(result, base, modulus)
        base = multiply_matrices(base, base, modulus)
        exponent >>= 1
    return result


# Short aliases are useful when demonstrating the algorithms interactively.
matrix_power_naive = naive_matrix_power
matrix_power_binary = binary_matrix_power


def fibonacci_modulo(index: int, modulus: int) -> int:
    """Return the ``index``th Fibonacci number modulo ``modulus``."""
    _validate_modulus(modulus)
    _validate_exponent(index)
    fibonacci_matrix = [[1, 1], [1, 0]]
    result = binary_matrix_power(fibonacci_matrix, index, modulus)
    return result[0][1]


def count_walks(
    adjacency_matrix: Sequence[Sequence[int]],
    source: int,
    destination: int,
    edges: int,
    modulus: int,
) -> int:
    """Count directed walks of exactly ``edges`` edges modulo ``modulus``.

    A matrix entry ``adjacency_matrix[u][v]`` represents the number of direct
    edges from vertex ``u`` to vertex ``v``.
    """
    _validate_modulus(modulus)
    _validate_exponent(edges)
    dimension = _validate_square_matrix(adjacency_matrix)
    if not 0 <= source < dimension or not 0 <= destination < dimension:
        raise IndexError("Source and destination must be valid vertex indices.")

    powered = binary_matrix_power(adjacency_matrix, edges, modulus)
    return powered[source][destination]


def compare_exponentiation(
    cases: Sequence[tuple[Sequence[Sequence[int]], int, int]],
) -> list[dict[str, object]]:
    """Compare both exponentiation methods for a sequence of test cases."""
    comparisons: list[dict[str, object]] = []
    for matrix, exponent, modulus in cases:
        naive = naive_matrix_power(matrix, exponent, modulus)
        binary = binary_matrix_power(matrix, exponent, modulus)
        comparisons.append({
            "matrix": [list(row) for row in matrix],
            "exponent": exponent,
            "modulus": modulus,
            "naive": naive,
            "binary": binary,
            "match": naive == binary,
        })
    return comparisons


def benchmark_exponentiation(
    dimensions: Sequence[int] = (2, 3, 4),
    exponents: Sequence[int] = (10, 100, 1_000),
    modulus: int = 1_000_003,
    seed: int = 302,
) -> list[dict[str, object]]:
    """Benchmark naive and binary exponentiation for several configurations."""
    _validate_modulus(modulus)
    if any(dimension <= 0 for dimension in dimensions):
        raise ValueError("Matrix dimensions must be positive.")
    if any(exponent < 0 for exponent in exponents):
        raise ValueError("Exponents cannot be negative.")

    generator = random.Random(seed)
    results: list[dict[str, object]] = []
    for dimension in dimensions:
        matrix = [
            [generator.randrange(modulus) for _ in range(dimension)]
            for _ in range(dimension)
        ]
        for exponent in exponents:
            start = time.perf_counter()
            naive_matrix_power(matrix, exponent, modulus)
            naive_seconds = time.perf_counter() - start

            start = time.perf_counter()
            binary_matrix_power(matrix, exponent, modulus)
            binary_seconds = time.perf_counter() - start

            results.append({
                "dimension": dimension,
                "exponent": exponent,
                "naive_seconds": naive_seconds,
                "binary_seconds": binary_seconds,
            })
    return results


def main() -> None:
    """Run comparisons, Fibonacci examples, walk counting, and benchmarks."""
    cases = [
        ([[1, 2], [3, 4]], 5, 100),
        ([[2, 1], [1, 2]], 10, 13),
        ([[0, 1], [1, 1]], 20, 1_000),
    ]
    print("Naive and binary matrix exponentiation comparison")
    for comparison in compare_exponentiation(cases):
        print(comparison)

    print("\nFibonacci numbers modulo 1,000,003")
    for index in (0, 1, 10, 100, 1_000_000):
        print(f"F({index}) =", fibonacci_modulo(index, 1_000_003))

    graph = [[0, 1, 1], [0, 0, 1], [1, 0, 0]]
    print("\nWalks from vertex 0 to vertex 2 in 4 edges:",
          count_walks(graph, 0, 2, 4, 1_000))

    print("\nBenchmark")
    for result in benchmark_exponentiation():
        print(result)


if __name__ == "__main__":
    main()