import sqlite3  # Untuk menghubungkan aplikasi dengan database SQLite
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk  # Untuk membangun antarmuka pengguna GUI

# Fungsi untuk membuat database dan tabel jika belum ada
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')  # Membuat/koneksi ke database
    cursor = conn.cursor()  # Membuat cursor untuk eksekusi query
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT,  
            biologi INTEGER,  
            fisika INTEGER,  
            inggris INTEGER,  
            prediksi_fakultas TEXT
        )
    ''')
    conn.commit()  # Menyimpan perubahan
    conn.close()  # Menutup koneksi

# Fungsi untuk mengambil data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")  # Mengambil semua data dari tabel
    rows = cursor.fetchall()  # Menyimpan semua baris data
    conn.close()
    return rows

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)  # Data dimasukkan sebagai parameter
    ''', (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?  # Berdasarkan ID
    ''', (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas berdasarkan nilai tertinggi
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menyimpan data dari form ke database
def submit():
    try:
        nama = nama_var.get()  # Mengambil nilai dari form
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:  # Validasi nama tidak kosong
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()  # Mengosongkan input
        populate_table()  # Memperbarui tabel
    except ValueError as e:
        messagebox.showerror("Error", f"Input tidak valid: {e}")

# Fungsi untuk memperbarui data berdasarkan ID
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil diperbarui!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk menghapus data berdasarkan ID
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())
        delete_database(record_id)
        messagebox.showinfo("Sukses", "Data berhasil dihapus!")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

# Fungsi untuk mengosongkan semua input form
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert('', 'end', values=row)  # Menambahkan data ke tabel

# Fungsi untuk mengisi form dengan data dari tabel
def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']

        selected_record_id.set(selected_row[0])  # Mengisi ID yang dipilih
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter untuk input data
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()  # Menyimpan ID data yang dipilih

# Membuat form input
Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Tombol aksi
Button(root, text="Add", command=submit).grid(row=4, column=0, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, pady=10)

# Membuat tabel
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
tree = ttk.Treeview(root, columns=columns, show='headings')

# Menyusun tabel
for col in columns:
    tree.heading(col, text=col.capitalize())
    tree.column(col, anchor='center') 

tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Event untuk mengisi form dari tabel
tree.bind('<ButtonRelease-1>', fill_inputs_from_table)

# Mengisi tabel dengan data awal
populate_table()

# Menjalankan aplikasi GUI
root.mainloop()
