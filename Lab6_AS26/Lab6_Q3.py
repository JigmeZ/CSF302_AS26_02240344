"""
Lab 6 - Question 3: Longest common subsequence.
"""

import itertools
import time


def lcs_table(x, y):
    table = [[0] * (len(y) + 1) for _ in range(len(x) + 1)]
    for i in range(1, len(x) + 1):
        for j in range(1, len(y) + 1):
            if x[i - 1] == y[j - 1]:
                table[i][j] = table[i - 1][j - 1] + 1
            else:
                table[i][j] = max(table[i - 1][j], table[i][j - 1])
    return table


def reconstruct_lcs(x, y, table):
    answer = []
    i, j = len(x), len(y)
    while i > 0 and j > 0:
        if x[i - 1] == y[j - 1]:
            answer.append(x[i - 1])
            i -= 1
            j -= 1
        elif table[i - 1][j] >= table[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(answer))


def lcs_length_two_rows(x, y):
    previous = [0] * (len(y) + 1)
    for character_x in x:
        current = [0] * (len(y) + 1)
        for j, character_y in enumerate(y, start=1):
            if character_x == character_y:
                current[j] = previous[j - 1] + 1
            else:
                current[j] = max(previous[j], current[j - 1])
        previous = current
    return previous[-1]


def brute_force_lcs_length(x, y):
    best = 0
    for size in range(len(x) + 1):
        for indexes in itertools.combinations(range(len(x)), size):
            subsequence = "".join(x[i] for i in indexes)
            if is_subsequence(subsequence, y):
                best = max(best, size)
    return best


def is_subsequence(shorter, longer):
    position = 0
    for character in longer:
        if position < len(shorter) and shorter[position] == character:
            position += 1
    return position == len(shorter)


def print_table(table, x, y):
    print("    " + " ".join(["-"] + list(y)))
    for i, row in enumerate(table):
        label = "-" if i == 0 else x[i - 1]
        print(f"{label}   " + " ".join(str(value) for value in row))


def print_line_diff(old_lines, new_lines):
    """Print unchanged lines, removed lines, and added lines."""
    table = lcs_table(old_lines, new_lines)
    common = reconstruct_lcs(old_lines, new_lines, table)
    old_index = new_index = 0
    for line in common:
        while old_lines[old_index] != line:
            print("- " + old_lines[old_index])
            old_index += 1
        while new_lines[new_index] != line:
            print("+ " + new_lines[new_index])
            new_index += 1
        print("  " + line)
        old_index += 1
        new_index += 1
    while old_index < len(old_lines):
        print("- " + old_lines[old_index])
        old_index += 1
    while new_index < len(new_lines):
        print("+ " + new_lines[new_index])
        new_index += 1


def compare_times():
    print("\nDP versus brute force")
    print("length,dp_seconds,brute_seconds")
    for length in range(5, 19):
        x = ("ABCBDAB" * 3)[:length]
        y = ("BDCABA" * 3)[:length]
        start = time.perf_counter()
        dp_answer = lcs_length_two_rows(x, y)
        dp_time = time.perf_counter() - start
        start = time.perf_counter()
        brute_answer = brute_force_lcs_length(x, y)
        brute_time = time.perf_counter() - start
        assert dp_answer == brute_answer
        print(f"{length},{dp_time:.6f},{brute_time:.6f}")


def main():
    x, y = "ABCBDAB", "BDCABA"
    table = lcs_table(x, y)
    print("LCS table")
    print_table(table, x, y)
    print("One LCS:", reconstruct_lcs(x, y, table))
    print("Two-row LCS length:", lcs_length_two_rows(x, y))
    compare_times()

    print("\nLine-by-line diff")
    old_file = ["one", "two", "three"]
    new_file = ["one", "new two", "three", "four"]
    print_line_diff(old_file, new_file)


if __name__ == "__main__":
    main()