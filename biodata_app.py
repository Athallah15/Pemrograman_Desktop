import tkinter as tk
from tkinter import messagebox

def submit_data():
    #cek checkbox
    if var_setuju.get() == 0:
        messagebox.showwarning("Peringatan", "Anda harus menyetujui syarat dan ketentuan.")
        return
    
    #ambil data dari form
    nama = entry_nama.get()
    nim = entry_nim.get()
    jurusan = entry_jurusan.get()
    jenis_kelamin = var_jk.get()

    #cek field kosong
    if not nama or not nim or not jurusan:
        messagebox.showwarning("Peringatan", "Semua field harus diisi.")
        return

    #tampilkan hasil
    hasil = f"Nama: {nama}\nNIM: {nim}\nJurusan: {jurusan}\nJenis Kelamin: {jenis_kelamin}"
    messagebox.showinfo("Data Tersimpan", hasil)

window = tk.Tk()
window.title("Form Biodata Mahasiswa")
window.geometry("500x600")
window.resizable(False, False)

#Membuat frame utama
main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

var_jk = tk.StringVar(value="pria")
# Variabel untuk checkbox
var_setuju = tk.IntVar()

label_judul = tk.Label(master=main_frame, text="Form Biodata Mahasiswa", font=("Arial", 16, "bold"))
label_judul.grid(row=0, column=0, columnspan=2, pady=20)

label_nama = tk.Label(master=main_frame,text="Nama Lengkap:", font=("Arial", 12))
label_nama.grid(row=1, column=0, sticky="W", pady=5)

entry_nama = tk.Entry(master=main_frame, width=30, font=("Calibri", 12))
entry_nama.grid(row=1, column=1, pady=5)

# Input NIM
label_nim = tk.Label(master=main_frame, text="NIM:", font=("Arial", 12))
label_nim.grid(row=2, column=0, sticky="W", pady=5)

entry_nim = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
entry_nim.grid(row=2, column=1, pady=5)

# Input Jurusan
label_jurusan = tk.Label(master=main_frame, text="Jurusan:", font=("Arial", 12))
label_jurusan.grid(row=3, column=0, sticky="W", pady=5)

entry_jurusan = tk.Entry(master=main_frame, width=30, font=("Arial", 12))
entry_jurusan.grid(row=3, column=1, pady=5)

# Label jenis kelamin
label_jk = tk.Label(master=main_frame, text="Jenis Kelamin:", font=("Arial", 12))
label_jk.grid(row=4, column=0, sticky="W", pady=5)

# Frame untuk radiobutton
frame_jk = tk.Frame(master=main_frame)
frame_jk.grid(row=4, column=1, sticky="W")

# Radiobutton pria dan wanita
radio_pria = tk.Radiobutton(master=frame_jk, text="Pria", variable=var_jk, value="Pria")
radio_pria.pack(side=tk.LEFT)

radio_wanita = tk.Radiobutton(master=frame_jk, text="Wanita", variable=var_jk, value="Wanita")
radio_wanita.pack(side=tk.LEFT)

#checkbox
check_setuju = tk.Checkbutton(
    master=main_frame,
    text="Saya menyetujui syarat dan ketentuan",
    variable=var_setuju,
    font=("Arial", 12)
)
check_setuju.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")   

# Tombol submit
btn_submit = tk.Button(
    master=main_frame, 
    text="Submit Biodata", 
    font=("Arial", 12, "bold"),
    command=submit_data
)
btn_submit.grid(row=6, column=0, columnspan=2, pady=20, sticky="EW")


# Mengatur lebar kolom agar label dan input sejajar
main_frame.columnconfigure(0, minsize=180)
main_frame.columnconfigure(1, weight=1)

window.configure(bg="#f0f0f0")
window.mainloop()