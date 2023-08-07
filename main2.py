import numpy as np

def metode_anp(array):
    selisih = 0.01
    is_first_calculation = True

    a = 2
    b = 1

    for i in range(len(array)):
        if len(array) == b + a:
            n = a + 1
            break
        b = b + a
        a = a + 1

    matriks = np.zeros((n, n))
    k = 0
    for i in range(n):
        for j in range(n):
            if matriks[i][j] is None:
                break 
            elif i == j:
                matriks[i][j] = 1
            elif j > i:
                matriks[i][j] = array[k]
                matriks[j][i] = 1 / array[k]
                k += 1

    while selisih < 0.05:
        if is_first_calculation:
            # Step awal membuat matriks kuadrat
            matriks = np.dot(matriks, matriks)
        else:
            # Step awal untuk perhitungan berikutnya
            matriks = np.dot(matriks, matriks)

        # Step 2 menjumlahkan matriks kuadrat
        sum_matriks = []
        for i in range(len(matriks)):
            jumlah = np.sum(matriks[i])
            sum_matriks.append(jumlah)
        
        # Menjumlahkan matriks yang sudah dijumlahkan
        sum_matriks_2 = np.sum(sum_matriks)

        # Step 3 membuat matriks normalized
        matriks_normalized = []
        for i in range(len(sum_matriks)):
            matriks_jumlah = sum_matriks[i] / sum_matriks_2
            matriks_normalized.append(matriks_jumlah)
         
        # Pengkondisian apakah perhitungan normalized yang pertama
        if is_first_calculation:
            is_first_calculation = False
            continue
        
        # Hitung selisih antara nilai matriks_normalized sekarang dan sebelumnya
        selisih = abs(matriks_normalized - matriks).max()

        # Assign nilai matriks_normalized ke array untuk perhitungan berikutnya
        array = matriks_normalized

    return matriks_normalized, matriks
# Definisikan input metode ANP
array = np.array([5,5,4,5,4,4,5,4,4,5])
 
matrix_normalized, matriks = metode_anp(array)

# Cetak hasil metode ANP
print("Hasil Metode ANP:")
print(matrix_normalized)
print("=====================================")
print("=====================================")
print("Hasil Metode ANP:")
print(matriks)
print("=====================================")