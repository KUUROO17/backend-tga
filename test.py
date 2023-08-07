@app.route('/data_per_alternatif/<int:id_user>', methods=['GET'])
def data_per_alternatif(id_user):
    url_penilaian = f"http://192.168.214.65:5000/penilaian/{id_user}"
    url_kriteria = "http://192.168.214.65:5000/data-kriteria"
    url_nilai_perbandingan = "http://192.168.214.65:5000/ambil_nilai_perbandingan"

    response_penilaian = requests.get(url_penilaian)
    response_kriteria = requests.get(url_kriteria)
    response_nilai_perbandingan = requests.get(url_nilai_perbandingan)

    if (
        response_penilaian.status_code == 200
        and response_kriteria.status_code == 200
        and response_nilai_perbandingan.status_code == 200
    ):
        data_penilaian = response_penilaian.json()
        data_kriteria = response_kriteria.json()
        status_kriteria = get_kriteria_status(data_kriteria["data"])
        grouped_data = group_values_by_alternatif(data_penilaian["data"])

        nilai_perbandingan = response_nilai_perbandingan.json()

        return jsonify({"data_per_alternatif": grouped_data, "status": status_kriteria, "nilai_bobot" : nilai_perbandingan})
    else:
        return jsonify({"error": "Gagal mendapatkan data dari API"}), 500

def group_values_by_alternatif(data):
    grouped_data = {}
    for item in data:
        id_alternatif = item["id_alternatif"]
        if id_alternatif not in grouped_data:
            grouped_data[id_alternatif] = []
        grouped_data[id_alternatif].append(item["nilai"])
    return list(grouped_data.values())

def get_kriteria_status(data):
    status_kriteria = {}
    for item in data:
        status_kriteria[item["nama"]] = item["status"]
    return list(status_kriteria.values())  # Mengubah nilai menjadi daftar