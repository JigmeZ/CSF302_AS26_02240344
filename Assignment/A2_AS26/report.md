# Assignment 2: Closest Camera Traps

## Part A: Implementation

`closest_pair_brute` checks all pairs. It returns the distance and the
original indices in increasing order. `closest_pair` sorts the points by
`x`, divides them into two halves, recursively solves both halves, and
checks the strip around the dividing line. Points are also kept sorted by
`y`, so the strip check takes linear time.

## Part B: Testing

`test_closest.py` checks the sample, two points, duplicate points, points on
one vertical line, a pair crossing the dividing line, and 500 seeded random
inputs containing 2 to 50 points. Every test compares the divide-and-conquer
answer with the brute-force answer.

## Part C: Analysis

The recurrence is:

```
T(n) = 2T(n/2) + Theta(n)
T(1) = Theta(1)
```

Here, the `2T(n/2)` term solves the two halves and `Theta(n)` sorts/filters
the points for the strip. By the Master Method, `a = 2`, `b = 2`, and
`f(n) = Theta(n)`. Since `n^(log_b(a)) = n`, this is Case 2:

```
T(n) = Theta(n log n)
```

The brute-force method has `Theta(n^2)` time and constant extra space
(apart from the result). The divide-and-conquer method has
`Theta(n log n)` time and `Theta(n)` extra space.

To collect timings, run:

```text
python timing.py
```

Use the resulting table for `n = 1000, 2000, 4000, ..., 64000`. Stop the
brute-force measurements when their total time exceeds 60 seconds. The
smallest row where the divide-and-conquer time is lower is the crossover
point on that machine. Small inputs may favour brute force because sorting
and recursion have larger constant costs.

## Part D: Critical reflection

The measured growth should eventually match the recurrence: brute force
grows quadratically, while divide and conquer grows close to `n log n`.
The measured times will not be exact because of Python overhead, sorting
constants, CPU load, and the fact that asymptotic notation describes large
inputs.

Brute force can be faster for small inputs even though its asymptotic
complexity is worse. For a small number of points, its nested loops are
simple, while divide and conquer must sort data and make recursive calls.
The crossover therefore depends on the computer and Python version.

The most important edge case is duplicate points, because its correct
distance is exactly zero and the original indices must still be returned.
The randomized tests compare both implementations, so an incorrect split or
strip boundary is likely to produce a failing test.

