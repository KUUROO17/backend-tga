import numpy as np
from fungsi import metode_anp, codas_norm

# Definisikan input metode ANP
array = np.array([2,3,2,2,2,2])
 
matrix_normalized = metode_anp(array)

# Cetak hasil metode ANP
print("Hasil Metode ANP:")
print(matrix_normalized)
print("=====================================")
print("=====================================")


# Gunakan hasil metode ANP sebagai bobot dalam metode CODAS
weights = matrix_normalized

# Definisikan input metode CODAS
alternatives = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6']
criteria = ['C1', 'C2', 'C3', 'C4']
statuses = ['Max', 'Min', 'Min', 'Max']

matrix_al = [[0.3,0.2,0.4,0.2],
             [0.4,0.3,0.3,0.3],
             [0.2,0.2,0.2,0.2],
             [0.6,0.3,0.2,0.2],
             [0.3,0.4,0.3,0.1],
             [0.2,0.1,0.2,0.2] ]

# Hitung metode CODAS
matriks_normalisasi, matriks_negatif, euclidian, taxicap, matriks_relativ_assesment, nilai_score = codas_norm(matrix_al, statuses, weights)

# Cetak hasil metode CODAS
print("Hasil Metode CODAS:")
print("Matriks Normalisasi:")
for row in matriks_normalisasi:
    print("  ".join(str(round(val, 2)) for val in row))
print("==============")
print("Matriks Ideal Negatif:")
print(matriks_negatif)
print("==============")
print("Matriks Euclidean:")
print(euclidian)
print("==============")
print("Matriks Taxicap:")
print(taxicap)
print("==============")

new_matrix = []
for i in range(len(matriks_relativ_assesment[0])):
    new_row = []
    for row in matriks_relativ_assesment:
        new_row.append(row[i])
    new_matrix.append(new_row)
    
print("Matriks Relatif Assessment:")
for row in new_matrix:
    print("  ".join(str(round(val, 10)) for val in row))
print("==================")
print("Nilai Assessment Score:")
print(nilai_score)