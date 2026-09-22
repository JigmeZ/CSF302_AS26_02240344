# Q1: Matrix Multiplication — Strassen's vs Traditional

import random
import time
import matplotlib.pyplot as plt


# Traditional Matrix Multiplication
def traditional(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]

    return C


# Strassen's Matrix Multiplication
def strassen(A, B):
    n = len(A)

    # Base case
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    mid = n // 2

    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    def add(X, Y):
        return [[X[i][j] + Y[i][j] for j in range(mid)]
                for i in range(mid)]

    def subtract(X, Y):
        return [[X[i][j] - Y[i][j] for j in range(mid)]
                for i in range(mid)]

    P1 = strassen(A11, subtract(B12, B22))
    P2 = strassen(add(A11, A12), B22)
    P3 = strassen(add(A21, A22), B11)
    P4 = strassen(A22, subtract(B21, B11))
    P5 = strassen(add(A11, A22), add(B11, B22))
    P6 = strassen(subtract(A12, A22), add(B21, B22))
    P7 = strassen(subtract(A11, A21), add(B11, B12))

    C11 = add(subtract(add(P5, P4), P2), P6)
    C12 = add(P1, P2)
    C21 = add(P3, P4)
    C22 = subtract(subtract(add(P5, P1), P3), P7)

    C = []

    for i in range(mid):
        C.append(C11[i] + C12[i])

    for i in range(mid):
        C.append(C21[i] + C22[i])

    return C


# Generate random matrix
def generate_matrix(n):
    return [[random.randint(1, 9) for _ in range(n)]
            for _ in range(n)]


# Display matrix
def display(A):
    for row in A:
        print(row)


# --------------------------------------------------
# PART 1: Test one matrix
# --------------------------------------------------

n = int(input("Enter matrix size (power of 2): "))

A = generate_matrix(n)
B = generate_matrix(n)

print("\nMatrix A:")
display(A)

print("\nMatrix B:")
display(B)


# Traditional
start = time.time()
C1 = traditional(A, B)
traditional_time = time.time() - start


# Strassen
start = time.time()
C2 = strassen(A, B)
strassen_time = time.time() - start


print("\nTraditional Result:")
display(C1)

print("\nStrassen Result:")
display(C2)

print("\nResults match:", C1 == C2)

print("\nTraditional Time:", traditional_time, "seconds")
print("Strassen Time:", strassen_time, "seconds")


# --------------------------------------------------
# PART 2: Collect data for graph
# --------------------------------------------------

sizes = [2, 4, 8, 16, 32, 64, 128]

traditional_times = []
strassen_times = []

print("\n\nRunning experiments for graph...")

for size in sizes:

    A = generate_matrix(size)
    B = generate_matrix(size)

    # Traditional
    start = time.time()
    traditional(A, B)
    t1 = time.time() - start

    # Strassen
    start = time.time()
    strassen(A, B)
    t2 = time.time() - start

    traditional_times.append(t1)
    strassen_times.append(t2)

    print("Size:", size)
    print("Traditional:", t1)
    print("Strassen:", t2)
    print()


# --------------------------------------------------
# PART 3: Display table
# --------------------------------------------------

print("\n===== TIME COMPARISON =====")
print("Size\tTraditional\tStrassen")

for i in range(len(sizes)):
    print(
        sizes[i],
        "\t",
        traditional_times[i],
        "\t",
        strassen_times[i]
    )


# --------------------------------------------------
# PART 4: Generate Graph
# --------------------------------------------------

plt.plot(
    sizes,
    traditional_times,
    marker='o',
    label='Traditional'
)

plt.plot(
    sizes,
    strassen_times,
    marker='o',
    label='Strassen'
)

plt.xlabel("Matrix Size")
plt.ylabel("Execution Time (seconds)")
plt.title("Traditional vs Strassen Matrix Multiplication")

plt.legend()
plt.grid(True)

plt.show()


#--------------------------------------------------
#--Analysis--
#The Traditional method uses three nested loops and has **O(n³)** time complexity. 
#Strassen's algorithm divides the matrices into smaller parts and uses 7 multiplications instead of 8, giving approximately **O(n²·⁸¹)** time complexity. 
#Both methods produces the same result. 
#As the matrix size increases, the difference in execution time becomes more noticeable.

# --Conclusion--
#Strassen's algorithm is more efficient than the traditional method for larger matrices.
#Strassen's algorithm can reduce the amount of multiplication work for large matrices, while the Traditional method is simpler to implement.
#------------------------------------------------