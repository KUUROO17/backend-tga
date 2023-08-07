import numpy as np

nilai = [2, 3, 2, 2, 2, 2]

a = 2
b = 1

for i in range(len(nilai)):
    if len(nilai) == b + a:
        n = a + 1
        break
    b = b + a
    a = a + 1

print(n)
matriks = np.zeros((n, n))
k = 0
for i in range(n):
    for j in range(n):
        if matriks[i][j] is None:
            break 
        elif i == j:
            matriks[i][j] = 1
        elif j > i:
            matriks[i][j] = nilai[k]
            matriks[j][i] = 1 / nilai[k]
            k += 1


print(matriks)
