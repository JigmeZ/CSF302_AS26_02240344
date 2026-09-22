import random
import time


# Traditional multiplication
def traditional_multiply(x, y):
    result = [0] * (len(x) + len(y))

    for i in range(len(x) - 1, -1, -1):
        for j in range(len(y) - 1, -1, -1):

            digit1 = int(x[i])
            digit2 = int(y[j])

            result[i + j + 1] += digit1 * digit2

    # Handle carry
    for i in range(len(result) - 1, 0, -1):
        result[i - 1] += result[i] // 10
        result[i] %= 10

    result = ''.join(map(str, result)).lstrip('0')

    return result if result else '0'


# Karatsuba multiplication
def karatsuba(x, y):

    # Remove leading zeros
    x = x.lstrip('0') or '0'
    y = y.lstrip('0') or '0'

    # Base case
    if len(x) == 1 and len(y) == 1:
        return str(int(x) * int(y))

    # Make lengths equal
    n = max(len(x), len(y))

    if n % 2 != 0:
        n += 1

    x = x.zfill(n)
    y = y.zfill(n)

    half = n // 2

    a = x[:half]
    b = x[half:]

    c = y[:half]
    d = y[half:]

    # Three recursive multiplications
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)

    a_plus_b = str(int(a) + int(b))
    c_plus_d = str(int(c) + int(d))

    middle = karatsuba(a_plus_b, c_plus_d)

    middle = int(middle) - int(ac) - int(bd)

    result = (int(ac) * (10 ** n)
              + middle * (10 ** half)
              + int(bd))

    return str(result)


# Generate random number
def generate_number(digits):
    number = str(random.randint(1, 9))

    for _ in range(digits - 1):
        number += str(random.randint(0, 9))

    return number


# Main program
digits = int(input("Enter number of digits: "))

x = generate_number(digits)
y = generate_number(digits)

print("\nNumber 1:", x)
print("Number 2:", y)

start = time.time()
result1 = traditional_multiply(x, y)
traditional_time = time.time() - start

start = time.time()
result2 = karatsuba(x, y)
karatsuba_time = time.time() - start

print("\nTraditional Result:", result1)
print("Karatsuba Result:", result2)

print("\nResults match:", result1 == result2)

print("\nTraditional Time:", traditional_time)
print("Karatsuba Time:", karatsuba_time)

#------------------------------------------------
#--Analysis--
#The Traditional multiplication method has **O(n²)** time complexity. 
#Karatsuba divides the numbers into smaller parts and uses only 3 multiplications instead of 4, giving approximately **O(n¹·⁵⁸⁵)** time complexity. 
#Both methods should produce the same result. 
#The advantage of Karatsuba becomes more noticeable as the number of digits increases.

#--Conclusion--
#Karatsuba can be more efficient for multiplying large integers because it reduces the number of recursive multiplications.
#------------------------------------------------