import json
from flask import Flask, jsonify, request, g
from flask_mysqldb import MySQL
from fungsi import metode_anp, codas_norm
import requests
import bcrypt

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tga-api'
mysql = MySQL(app)



#register user

# Fungsi untuk melakukan hashing bcrypt pada password
def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Fungsi untuk melakukan registrasi user
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    nama = data['nama']
    username = data['username']
    password = data['password']

    # Enkripsi password menggunakan bcrypt
    hashed_password = hash_password(password)

    try:
        cur = mysql.connection.cursor()
        # Simpan data user ke dalam tabel
        cur.execute("INSERT INTO user (nama, username, password) VALUES (%s, %s, %s)",
                    (nama, username, hashed_password))
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Registrasi berhasil'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Fungsi untuk melakukan login user
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']
    

    try:
        cur = mysql.connection.cursor()
        # Ambil data user berdasarkan username
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user:
            # Verifikasi password yang diinputkan dengan password di database
            if bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
                id_user = user[0]
                nama_user = user[1]
                rule = user[4]
                return jsonify({'message': 'Login berhasil', 'id_user': id_user, 'nama': nama_user, 'rule': rule }), 200
            else:
                return jsonify({'message': 'Password salah'}), 401
        else:
            return jsonify({'message': 'Username tidak ditemukan'}), 404
    except Exception as e:
        return jsonify({'error': 'Terjadi kesalahan'}), 500



@app.route('/user/<int:id>', methods=['GET'])
def lihat_user(id):
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM user WHERE id = %s''', (id, ))
    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)

@app.route('/user/<int:id>', methods=['PUT'])
def edit_user(id):
    if request.method == 'PUT':
        try:
            cur = mysql.connection.cursor()

            # Mendapatkan data user berdasarkan ID
            cur.execute('''SELECT * FROM user WHERE id = %s''', (id,))
            data = cur.fetchone()

            if data is None:
                return jsonify({'message': 'Data user tidak ditemukan'}), 404

            # Mendapatkan data yang dikirim dalam body request
            json_data = request.get_json()
            username = json_data.get('username')
            name = json_data.get('name')
            # Jika ada data lain yang ingin diubah, sesuaikan di sini

            # Update data user berdasarkan ID
            cur.execute('''UPDATE user SET username = %s, nama = %s WHERE id = %s''', (username, name, id))
            mysql.connection.commit()
            cur.close()

            return jsonify({'message': 'Data user berhasil diupdate'}), 200

        except Exception as e:
            return jsonify({'message': 'Terjadi kesalahan saat mengupdate data user', 'error': str(e)}), 500


#kriteria
#menampilkan data
@app.route('/data-kriteria', methods=['GET'])
def get_data():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM kriteria''')

    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)


#menambahkan data
@app.route('/data-kriteria', methods=['POST'])
def add_data():
    cur = mysql.connection.cursor()
    kode = request.json['kode']
    nama = request.json['nama']
    status = request.json['status']
    print(status)
    cur.execute('''INSERT INTO kriteria (kode, nama, status) VALUES (%s, %s, %s)''', (kode, nama, status))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data added successfully'})

#mengubah data
@app.route('/data-kriteria/<kode>', methods=['PUT'])
def update_data(kode):
    cur = mysql.connection.cursor()
    nama = request.json['nama']
    status = request.json['status']
    cur.execute('''UPDATE kriteria SET nama = %s, status = %s WHERE kode = %s''', (nama, status, kode))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data updated successfully'})

#menghapus data
@app.route('/data-kriteria/<kode>', methods=['DELETE'])
def delete_data(kode):
    cur = mysql.connection.cursor()
    cur.execute('''DELETE FROM kriteria WHERE kode = %s''', (kode,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Data deleted successfully'})


@app.route('/data-alternatif/<int:id_user>', methods=['GET'])
def data_alternatif(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alternatif where id_user = %s', (id_user,))

    
    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)

@app.route('/data-alternatif-kode/<kode>', methods=['GET'])
def data_alternatif_lihat(kode):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM alternatif WHERE kode = %s', (kode,))

    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)

@app.route('/data-alternatif-hasil/<int:id_user>', methods=['GET'])
def data_alternatif_lihat_hasil(id_user):
    try:
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM hasil WHERE id_user=%s', (id_user,))

        # Mendapatkan nama kolom dari atribut description
        column_names = [desc[0] for desc in cur.description]

        data = cur.fetchall()
        cur.close()

        result = {
            'data': []
        }

        for row in data:
            row_dict = {}
            for i in range(len(column_names)):
                row_dict[column_names[i]] = row[i]
            result['data'].append(row_dict)

        return jsonify(result)
    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "Terjadi kesalahan"}), 500




#menambahkan data alternatif
@app.route('/data-alternatif', methods=['POST'])
def add_data_alternatif():
    try:
        # Ambil data yang dikirimkan dalam request
        data = request.json

        # Pastikan data yang dibutuhkan tersedia dalam request
        if 'kode' not in data or 'nama' not in data or 'alamat' not in data or 'id_user' not in data:
            return jsonify({"message": "Data yang diperlukan tidak lengkap"}), 400

        # Ekstrak nilai dari data request
        kode = data['kode']
        nama = data['nama']
        alamat = data['alamat']
        id_user = data['id_user']

        # Periksa apakah id_user tersebut ada dalam tabel user
        cur = mysql.connection.cursor()
        cur.execute('''SELECT * FROM user WHERE id = %s''', (id_user,))
        user = cur.fetchone()
        cur.close()

        if not user:
            return jsonify({"message": "User dengan id tersebut tidak ditemukan"}), 404

        # Tambahkan data ke dalam tabel alternatif
        cur = mysql.connection.cursor()
        cur.execute('''INSERT INTO alternatif (kode, nama, alamat, id_user) VALUES (%s, %s, %s, %s)''', (kode, nama, alamat, id_user))
        mysql.connection.commit()
        cur.close()

        return jsonify({"message": "Data berhasil ditambahkan"}), 201

    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "Terjadi kesalahan"}), 500
    
@app.route('/data-alternatif/<kode>', methods=['PUT'])
def edit_data_alternatif(kode):
    try:
        # Ambil data yang dikirimkan dalam request
        data = request.json

        # Pastikan data yang dibutuhkan tersedia dalam request
        if 'kode' not in data or 'nama' not in data or 'alamat' not in data:
            return jsonify({"message": "Data yang diperlukan tidak lengkap"}), 400

        # Ekstrak nilai dari data request
        kode = data['kode']
        nama = data['nama']
        alamat = data['alamat']
        userId = data['user_id']
        print(alamat)

        # Membuat koneksi ke database
        cur = mysql.connection.cursor()

        # Edit data alternatif berdasarkan id/
        result = cur.execute('UPDATE alternatif SET kode = %s, nama = %s, alamat = %s, id_user = %s  WHERE kode=%s',
                    (kode, nama, alamat, userId, kode))
        mysql.connection.commit()

        # Menutup cursor dan koneksi ke database
        cur.close()

        return jsonify({"message": "Data berhasil diupdate"}), 200

    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "Terjadi kesalahan"}), 500

# Endpoint untuk menghapus data alternatif berdasarkan id (method DELETE)
@app.route('/data-alternatif/<kode>', methods=['DELETE'])
def delete_data_alternatif(kode):
    try:
        # Membuat koneksi ke database
        cur = mysql.connection.cursor()

        # Hapus data alternatif berdasarkan id
        cur.execute('DELETE FROM alternatif WHERE kode = %s', (kode,))
        mysql.connection.commit()


        # Menutup cursor dan koneksi ke database
        cur.close()

        return jsonify({"message": "Data berhasil dihapus"}), 200

    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "Terjadi kesalahan"}), 500



#menambahkan nilai perbandingan antar kriteria 
@app.route('/simpan_perbandingan', methods=['GET'] )
def view_perbandingan():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM nilai_kriteria''')

    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)

#menambahkan data perbandingan
@app.route('/simpan_perbandingan', methods=['POST'])
def simpan_perbandingan():
    data = request.json

    try:
        for item in data:
            kriteria1 = item['kriteria1']
            kriteria2 = item['kriteria2']
            nilai_perbandingan = item['nilai_perbandingan']

            cur = mysql.connection.cursor()
            # Simpan data perbandingan ke dalam tabel
            cur.execute("INSERT INTO nilai_kriteria (kriteria1, kriteria2, nilai_perbandingan) VALUES (%s, %s, %s)", (kriteria1, kriteria2, nilai_perbandingan))
            mysql.connection.commit()
            cur.close()

        return jsonify({'message': 'Data perbandingan berhasil disimpan'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# mengubah nilai perbandingan
@app.route('/simpan_perbandingan/<int:id>', methods=['PUT'])
def update_nilai_perbandingan(id):
    try:
        cur = mysql.connection.cursor()
        # Ambil nilai_perbandingan dari body permintaan yang dikirim oleh frontend
        nilai = request.json['nilai_perbandingan']
        # Perbarui data di tabel nilai_kriteria berdasarkan ID yang diberikan
        cur.execute('UPDATE nilai_kriteria SET nilai_perbandingan = %s WHERE id = %s', (nilai, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Data updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update data', 'error': str(e)}), 500


# menghapus semua nilai perbandingan
@app.route('/hapus_semua_perbandingan', methods=['DELETE'])
def hapus_semua_perbandingan():
    try:
        cur = mysql.connection.cursor()
        # Hapus semua data perbandingan dari tabel
        cur.execute("DELETE FROM nilai_kriteria")
        mysql.connection.commit()
        cur.close()

        return jsonify({'message': 'Semua nilai perbandingan berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# @app.route('/test-ambil', methods=['GET'])
# def cok():
#     cur = mysql.connection.cursor()
#     cur.execute('''SELECT kode FROM kriteria''')

#     # Mendapatkan nama kolom dari atribut description
#     column_names = [desc[0] for desc in cur.description]

#     data = cur.fetchall()
#     cur.close()

#     result = {
#         'data': []
#     }

#     for row in data:
#         row_dict = {}
#         for i in range(len(column_names)):
#             row_dict[column_names[i]] = row[i]
#         result['data'].append(row_dict)

#     return jsonify(result)


#untuk menambahkan nilai bobot ke dalam tabel
@app.route('/ambil_nilai_perbandingan', methods=['GET'])
def ambil_nilai_perbandingan():
    try:
        # Retrieve kriteria data from the kriteria table
        cur = mysql.connection.cursor()
        cur.execute("SELECT kode FROM kriteria")
        data_kriteria = cur.fetchall()
        cur.close()

        # Retrieve perbandingan data from the nilai_kriteria table
        cur = mysql.connection.cursor()
        cur.execute("SELECT nilai_perbandingan FROM nilai_kriteria")
        data_perbandingan = cur.fetchall()
        cur.close()

        nilai_perbandingan = [item[0] for item in data_perbandingan]

        # Process perbandingan data and add id_kriteria based on kode
        matrix_normalized = metode_anp(nilai_perbandingan)
        for i, value in enumerate(matrix_normalized):
            kode_kriteria = data_kriteria[i][0]
            
            # Retrieve id_kriteria based on kode_kriteria
            cur = mysql.connection.cursor()
            cur.execute(f"SELECT kode FROM kriteria WHERE kode = '{kode_kriteria}'")
            result = cur.fetchone()
            cur.close()

            if result:
                id_kriteria = result[0]
                
                # Check if bobot value for kriteria exists in nilai_bobot table
                cur = mysql.connection.cursor()
                cur.execute(f"SELECT id_kriteria FROM nilai_bobot WHERE id_kriteria = '{id_kriteria}'")
                existing_bobot = cur.fetchone()
                cur.close()

                if existing_bobot:
                    # If bobot value exists, update bobot value
                    update_query = f"UPDATE nilai_bobot SET value = {value} WHERE id_kriteria = '{id_kriteria}'"
                    cur = mysql.connection.cursor()
                    cur.execute(update_query)
                    mysql.connection.commit()
                    cur.close()
                else:
                    # If bobot value doesn't exist, insert bobot value
                    insert_query = f"INSERT INTO nilai_bobot (id_kriteria, value) VALUES ('{id_kriteria}', {value})"
                    cur = mysql.connection.cursor()
                    cur.execute(insert_query)
                    mysql.connection.commit()
                    cur.close()

        return jsonify(matrix_normalized)

    except mysql.connector.Error as err:
        return jsonify({'error': f'Error while accessing database: {str(err)}'})

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})




@app.route('/penilaian', methods=['POST'])
def tambah_penilaian():
    try:
        data = request.json
    
        # Pastikan data yang dibutuhkan tersedia dalam request
        if 'id_alternatif' not in data or 'nilai' not in data:
            return jsonify({"message": "Data yang diperlukan tidak lengkap"}), 400

        print(data)
        id_user = data['id_user']
        id_alternatif = data['id_alternatif']
        nilai = json.loads(data['nilai'])  # Ubah nilai menjadi objek Python

        # Ambil id_kriteria dan nilai dari setiap elemen di dalam nilai
        for id_kriteria, nilai_kriteria in nilai.items():
            print("id_kriteria:", id_kriteria)
            print("nilai:", nilai_kriteria)

            # embuat koneksi ke database
            cur = mysql.connection.cursor()
                
            # Memasukkan data penilaian ke dalam tabel "penilaian"
            cur.execute("INSERT INTO penilaian (id_kriteria, id_alternatif, nilai, id_user) VALUES (%s, %s, %s, %s)", (id_kriteria, id_alternatif, nilai_kriteria, id_user))
            mysql.connection.commit()

            # Menutup cursor
            cur.close()

        return jsonify({"message": "Data penilaian berhasil disimpan"}), 201

    except Exception as e:
        print('Error:', e)
        return jsonify({"message": "Terjadi kesalahan"}), 500
    

@app.route('/penilaian/<int:id_user>', methods=['GET'] )
def view_nilai(id_user):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM penilaian where id_user = %s', (id_user,))

    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)

@app.route('/penilaian/<int:id>', methods=['PUT'])
def update_nilai_penilaian(id):
    try:
        cur = mysql.connection.cursor()
        nilai = request.json['nilai']
        print(f"Received data: ID: {id}, Nilai: {nilai}")
        cur.execute('UPDATE penilaian SET nilai = %s WHERE id = %s', (nilai, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Nilai Penilaian Berhasil Diupdate"}), 200
    except Exception as e:
        return jsonify({'message': 'Gagal mengupdate data', 'error': str(e)}), 500


@app.route('/hapus_penilaian/<id_user>', methods=['DELETE'])
def hapus_semua_penilaian(id_user):
    try:
        cur = mysql.connection.cursor()
        # Menghapus seluruh isi pada table penilaian dan hasil_ak
        cur.execute("DELETE FROM penilaian WHERE id_user = %s", (id_user ,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Semua nilai perbandingan berhasil dihapus'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

@app.route('/metode_kodas/<int:id_user>/<id_alternatif>', methods=['GET'])
def metodeKODAS(id_user, id_alternatif):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM penilaian WHERE id_user = %s AND id_alternatif = %s', (id_user, id_alternatif))

    # Mendapatkan nama kolom dari atribut description setelah query dieksekusi
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)




# @app.route('/data_per_alternatif/<int:id_user>', methods=['GET'])
# def data_per_alternatif(id_user):
#     try:
#         # Mengambil data penilaian dari tabel penilaian
#         cur = mysql.connection.cursor()
#         cur.execute(f"SELECT id_alternatif,nilai FROM penilaian WHERE id_user = {id_user}")
#         data_penilaian = cur.fetchall()
#         cur.close()

#         # Mengambil data kriteria dari tabel kriteria
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT nama, status FROM kriteria")
#         data_kriteria = cur.fetchall()
#         cur.close()

#         status_kriteria = get_kriteria_status(data_kriteria)
#         grouped_data = group_values_by_alternatif(data_penilaian)

#         # Mengambil data nilai bobot dari tabel nilai_bobot
#         cur = mysql.connection.cursor()
#         cur.execute("SELECT value FROM nilai_bobot")
#         nilai_perbandingan = [item[0] for item in cur.fetchall()]
#         cur.close()

#         matriks_normalisasi, matriks_negatif, euclidian, taxicap, matriks_relativ_assesment, nilai_score = codas_norm(grouped_data, status_kriteria, nilai_perbandingan)

#         cur = mysql.connection.cursor()
#         cur.execute(f"SELECT kode FROM alternatif WHERE id_user = {id_user}")
#         result = cur.fetchall()

#         for i, nilai in enumerate(nilai_score):
#             if i < len(result):
#                 kode_alternatif = result[i][0]
#                 id_alternatif = kode_alternatif
#                 cur.execute(f"SELECT * FROM hasil WHERE id_user = {id_user} AND id_alternatif = '{id_alternatif}'")
#                 existing_data = cur.fetchone()
#                 if existing_data:
#                     update_query = f"UPDATE hasil SET value = '{nilai}' WHERE id_user = {id_user} AND id_alternatif = '{id_alternatif}'"
#                     cur.execute(update_query)
#                 else:
#                     insert_query = f"INSERT INTO hasil (id_user, id_alternatif, value) VALUES ({id_user}, '{id_alternatif}', '{nilai}')"
#                     cur.execute(insert_query)

#         mysql.connection.commit()
#         cur.close()

#         return jsonify({"matriks_normalisasi": matriks_normalisasi, "matriks_negatif": matriks_negatif, "euclidian": euclidian, "taxicap": taxicap, "matriks_relativ_assesment": matriks_relativ_assesment, "nilai score": nilai_score})
#     except mysql.connector.Error as err:
#         return jsonify({'error': f'Error while accessing database: {str(err)}'})
#     except Exception as e:
#         return jsonify({'error': f'An error occurred: {str(e)}'})


@app.route('/data_per_alternatif/<int:id_user>', methods=['GET'])
def data_per(id_user):
    try:
        # Mengambil data penilaian dari tabel penilaian
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT id_alternatif, nilai FROM penilaian WHERE id_user = {id_user}")
        data_penilaian = cur.fetchall()
        cur.close()

        # Mengambil data kriteria dari tabel kriteria
        cur = mysql.connection.cursor()
        cur.execute("SELECT nama, status FROM kriteria")
        data_kriteria = cur.fetchall()
        cur.close()

        # Mengambil data nilai bobot dari tabel nilai_bobot
        cur = mysql.connection.cursor()
        cur.execute("SELECT value FROM nilai_bobot")
        nilai_perbandingan = [item[0] for item in cur.fetchall()]
        cur.close()

        # Memperbaiki pemrosesan status kriteria dan pengelompokan data
        status_kriteria = get_kriteria_status(data_kriteria)
        grouped_data = group_values_by_alternatif(data_penilaian)
        print(grouped_data)
        print(status_kriteria)

        matriks_normalisasi, matriks_negatif, euclidian, taxicap, matriks_relativ_assesment, nilai_score = codas_norm(grouped_data, status_kriteria, nilai_perbandingan)

        cur = mysql.connection.cursor()
        cur.execute(f"SELECT kode FROM alternatif WHERE id_user = {id_user}")
        result = cur.fetchall()

        for i, nilai in enumerate(nilai_score):
            if i < len(result):
                kode_alternatif = result[i][0]
                id_alternatif = kode_alternatif
                cur.execute(f"SELECT * FROM hasil WHERE id_user = {id_user} AND id_alternatif = '{id_alternatif}'")
                existing_data = cur.fetchone()
                if existing_data:
                    update_query = f"UPDATE hasil SET value = '{nilai}' WHERE id_user = {id_user} AND id_alternatif = '{id_alternatif}'"
                    cur.execute(update_query)
                else:
                    insert_query = f"INSERT INTO hasil (id_user, id_alternatif, value) VALUES ({id_user}, '{id_alternatif}', '{nilai}')"
                    cur.execute(insert_query)

        mysql.connection.commit()
        cur.close()
        # return jsonify({"data_penilaian": data_penilaian, "data_kriteria": data_kriteria, "nilai_perbandingan": nilai_perbandingan})
        return jsonify({"matriks_normalisasi": matriks_normalisasi, "matriks_negatif": matriks_negatif, "euclidian": euclidian, "taxicap": taxicap, "matriks_relativ_assesment": matriks_relativ_assesment, "nilai score": nilai_score})
    except mysql.connector.Error as err:
        return jsonify({'error': f'Error while accessing database: {str(err)}'})
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'})

def group_values_by_alternatif(data):
    grouped_data = {}
    for item in data:
        id_alternatif = item[0]  # Menggunakan index 0 untuk id_alternatif
        nilai = item[1]  # Menggunakan index 1 untuk nilai
        if id_alternatif not in grouped_data:
            grouped_data[id_alternatif] = []
        grouped_data[id_alternatif].append(nilai)
    return list(grouped_data.values())


def get_kriteria_status(data):
    status_kriteria = {}
    for item in data:
        nama_kriteria = item[0]  # Menggunakan index 0 untuk nama
        status = item[1]  # Menggunakan index 1 untuk status
        status_kriteria[nama_kriteria] = status
    return list(status_kriteria.values())



@app.route('/lihat-penilaian', methods=['GET'])
def lihat_penilaian():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM penilaian''')

    # Mendapatkan nama kolom dari atribut description
    column_names = [desc[0] for desc in cur.description]

    data = cur.fetchall()
    cur.close()

    result = {
        'data': []
    }

    for row in data:
        row_dict = {}
        for i in range(len(column_names)):
            row_dict[column_names[i]] = row[i]
        result['data'].append(row_dict)

    return jsonify(result)





if __name__ == '__main__':
    app.run(debug=True, host='192.168.239.65', port=5000)