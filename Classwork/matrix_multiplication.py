# solving 2 * 2 matrics in very simple way
# SQUARE MATRIX MULTIPLICATION(A, B)
# let n = 2
A = [
    [1, 2],
    [3, 4]
    ]

B = [
    [5, 6],
    [7, 8]
    ]

# this is the result matrix C which will store the result of A * B
C = [
    [0, 0],
    [0, 0]
    ]

for i in range(2):
    for j in range(2):
        C[i][j]    = 0
        for k in range(2):
            C[i][j] += A[i][k] * B[k][j]

print(C)  

