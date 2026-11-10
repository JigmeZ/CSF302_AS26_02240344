import time


# Check whether the exponent and modulus are valid.
def check_input(exponent, modulus):
    if exponent < 0:
        raise ValueError("The exponent cannot be negative.")

    if modulus <= 0:
        raise ValueError("The modulus must be greater than zero.")


# Naive method:
# Multiply the base by itself one exponent number of times.
def naive_power(base, exponent, modulus):
    check_input(exponent, modulus)

    answer = 1

    for count in range(exponent):
        answer = (answer * base) % modulus

    return answer


# Binary method:
# Use square and multiply to reduce the number of calculations.
def binary_power(base, exponent, modulus):
    check_input(exponent, modulus)

    answer = 1
    base = base % modulus

    while exponent > 0:
        # If the last binary bit is 1, the exponent is odd.
        if exponent & 1:
            answer = (answer * base) % modulus

        # Square the base for the next step.
        base = (base * base) % modulus

        # Shift right by one bit, which divides the exponent by 2.
        exponent = exponent >> 1

    return answer


# Compare both methods for one set of values.
def compare_answers(base, exponent, modulus):
    first_answer = naive_power(base, exponent, modulus)
    second_answer = binary_power(base, exponent, modulus)

    print("Base:", base, "Exponent:", exponent, "Modulus:", modulus)
    print("Naive answer: ", first_answer)
    print("Binary answer:", second_answer)
    print("Answers match:", first_answer == second_answer)


# Test different bases, exponents, and moduli.
def test_different_values():
    print("\nComparing different values")

    test_values = [
        (2, 10, 1000),
        (5, 7, 13),
        (-3, 4, 11),
        (10, 0, 7)
    ]

    for base, exponent, modulus in test_values:
        compare_answers(base, exponent, modulus)
        print()


# Compare the execution time of both methods.
def compare_times(base, modulus):
    print("Execution time comparison")
    print("Exponent\tNaive time\tBinary time")

    # Larger exponents make the difference easier to see.
    exponents = [10, 100, 1000, 10000, 100000]

    for exponent in exponents:
        start_time = time.perf_counter()
        naive_power(base, exponent, modulus)
        naive_time = time.perf_counter() - start_time

        start_time = time.perf_counter()
        binary_power(base, exponent, modulus)
        binary_time = time.perf_counter() - start_time

        print(f"{exponent}\t\t{naive_time:.8f}\t{binary_time:.8f}")


def main():
    print("Efficient Modular Exponentiation")

    # First show that both algorithms work for different values.
    test_different_values()

    try:
        print("Enter your own values")
        base = int(input("Enter the base: "))
        exponent = int(input("Enter the exponent (0 or greater): "))
        modulus = int(input("Enter the modulus (greater than 0): "))

        print("\nYour result")
        compare_answers(base, exponent, modulus)

        print()
        compare_times(base, modulus)

    except ValueError as error:
        # Show a message when the user enters an invalid value.
        print("Invalid input:", error)


if __name__ == "__main__":
    main()
