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

    return matriks_normalized

def codas_norm(matrix_al, statuses, weights):
   
   #code untuk membalikkan array guna untuk mengambil nilai per kriteria
    matrix = []
    for i in range(len(matrix_al[0])):
        new_row = []
        for row in matrix_al:
            new_row.append(row[i])
        matrix.append(new_row)

    # mencari matriks normalisasi
    matriks_normalisasi = []
    for i in range(len(statuses)):
        if statuses[i] == "Max":
            temp = []
            for k in range(len(matrix[i])):
                hasil = matrix[i][k] / max(matrix[i]) * weights[i]
                temp.append(hasil)
            matriks_normalisasi.append(temp)
        else:
            temp = []
            for k in range(len(matrix[i])):
                hasil = min(matrix[i]) / matrix[i][k] * weights[i]
                temp.append(hasil)
            matriks_normalisasi.append(temp)

    # mencari nilai terkecil / matriks ideal negatif
    matriks_negatif = []
    for i in range(len(matriks_normalisasi)):
        nilai_kecil = min(matriks_normalisasi[i])
        matriks_negatif.append(nilai_kecil)

    # ubah baris matrix normalisasi dari atas ke bawah
    matriks_normalisasi_np = np.array(matriks_normalisasi)
    matriks_normalisasi_ubah = []
    for i in range(matriks_normalisasi_np.shape[1]):
        nilai_index = matriks_normalisasi_np[:, i]
        matriks_normalisasi_ubah.append(nilai_index)

    # mencari nilai matrix euclidian
    euclidian = []

    for i in range(len(matriks_normalisasi_ubah)):
        # menghitung selisih antara 2 set data
        selisih = np.subtract(matriks_normalisasi_ubah[i], matriks_negatif)
        # Menghitung jumlah kuadrat selisih
        hasil_kuadrat = np.sum(np.square(selisih))
        # Menghitung akar kuadrat dari jumlah kuadrat selisih
        hasil = np.sqrt(hasil_kuadrat)
        euclidian.append(hasil)
    
    #mencari nilai dari matrix taxicap
    taxicap = []
    for i in range (len(matriks_normalisasi_ubah)):
        temp = 0
        for j in range(len(matriks_normalisasi_ubah[i])):
            temp += abs(matriks_normalisasi_ubah[i][j]- matriks_negatif[j])
        taxicap.append(temp)
    
    # matriks relatif assesment
    phi = 0.02
    # variabel matriks relativ assesment
    matriks_relativ_assesment = []
    for i in range(len(euclidian)):
        temp = []
        for j in range(len(euclidian)):
            rumus = (euclidian[j] - euclidian[i]) + (phi * (euclidian[j] - euclidian[i]) * (taxicap[j] - taxicap[i]))
            temp.append(rumus)
        matriks_relativ_assesment.append(temp)
    
    #membalikkan matriks relatif assesment 
    
    new_mra = []
    for i in range(len(matriks_relativ_assesment[0])):
        new_row = []
        for row in matriks_relativ_assesment:
            new_row.append(row[i])
        new_mra.append(new_row)

    #menjumlahkan per baris matrix relatif assesment
    new_row_sum = np.sum(new_mra, axis=1)

    # menjumlahkan nilai setiap array matriks relativ assesment
    nilai_score = []
    for i in range(len(matriks_relativ_assesment[0])):
        jumlah = sum(row[i] for row in matriks_relativ_assesment)
        nilai_score.append(jumlah)
    

    return matriks_normalisasi, matriks_negatif, euclidian, taxicap, matriks_relativ_assesment, nilai_score