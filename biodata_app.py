import tkinter as tk
from tkinter import messagebox


# Membuat kelas utama aplikasi yang mewarisi dari tk.Tk
class AplikasiBiodata(tk.Tk):

    # Metode __init__ adalah constructor yang akan dijalankan saat objek dibuat
    def __init__(self):
        super().__init__()

        # Mengkonfigurasi window utama
        self.title("Aplikasi Biodata Mahasiswa")
        self.geometry("600x700")
        self.resizable(True, True)

        # Database user sederhana (dalam aplikasi nyata, ini akan di database)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456"
        }

        # Status login
        self.current_user = None

        # Atribut untuk manajemen frame
        self.frame_aktif = None

        # Buat tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Tampilkan frame login di awal
        self._pindah_ke(self.frame_login)

    # ==========================================
    # Tampilan Login
    # ==========================================
    def _buat_tampilan_login(self):

        # Frame login
        self.frame_login = tk.Frame(
            master=self,
            padx=30,
            pady=30
        )

        self.frame_login.columnconfigure(1, weight=1)

        # Judul Login
        self.label_login = tk.Label(
            master=self.frame_login,
            text="LOGIN APLIKASI",
            font=("Arial", 18, "bold")
        )
        self.label_login.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=30
        )

        # Username
        self.label_username = tk.Label(
            master=self.frame_login,
            text="Username:",
            font=("Arial", 12)
        )
        self.label_username.grid(
            row=1,
            column=0,
            sticky="W",
            pady=10
        )

        self.entry_username = tk.Entry(
            master=self.frame_login,
            width=30,
            font=("Arial", 12)
        )
        self.entry_username.grid(
            row=1,
            column=1,
            pady=10
        )

        # Password
        self.label_password = tk.Label(
            master=self.frame_login,
            text="Password:",
            font=("Arial", 12)
        )
        self.label_password.grid(
            row=2,
            column=0,
            sticky="W",
            pady=10
        )

        self.entry_password = tk.Entry(
            master=self.frame_login,
            width=30,
            font=("Arial", 12),
            show="*"
        )
        self.entry_password.grid(
            row=2,
            column=1,
            pady=10
        )

        # Tombol Login
        self.btn_login = tk.Button(
            master=self.frame_login,
            text="Login",
            font=("Arial", 12, "bold"),
            command=self._coba_login
        )
        self.btn_login.grid(
            row=3,
            column=0,
            columnspan=2,
            pady=20,
            sticky="EW"
        )

        # Shortcut Enter
        self.entry_username.bind(
            "<Return>",
            self._coba_login
        )

        self.entry_password.bind(
            "<Return>",
            self._coba_login
        )

    # ==========================================
    # Fungsi Login
    # ==========================================
    def _coba_login(self, event=None):
        """Method untuk memproses attempt login"""

        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        # Validasi input kosong
        if not username or not password:
            messagebox.showwarning(
                "Login Gagal",
                "Username dan Password tidak boleh kosong."
            )
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            messagebox.showwarning(
                "Login Gagal",
                "Username minimal 3 karakter."
            )
            self.entry_username.focus_set()
            return

        # Cek username dan password
        if username in self.users_db and self.users_db[username] == password:

            # Simpan user yang sedang login
            self.current_user = username

            messagebox.showinfo(
                "Login Berhasil",
                f"Selamat datang, {username}!"
            )

            # Pindah ke form biodata
            self._pindah_ke(self.frame_biodata)

        else:
            messagebox.showerror(
                "Login Gagal",
                "Username atau Password salah."
            )

    # ==========================================
    # Tampilan Biodata
    # ==========================================
    def _buat_tampilan_biodata(self):

        # ==============================
        # Variabel Kontrol Tkinter
        # ==============================
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar()

        # ==============================
        # Frame Utama
        # ==============================
        self.main_frame = tk.Frame(
            master=self,
            padx=20,
            pady=20
        )

        self.main_frame.pack(
            fill=tk.BOTH,
            expand=True
        )

        # Mengatur lebar kolom
        self.main_frame.columnconfigure(
            0,
            minsize=180
        )

        self.main_frame.columnconfigure(
            1,
            weight=1
        )

        # ==============================
        # Judul
        # ==============================
        self.label_judul = tk.Label(
            master=self.main_frame,
            text="Form Biodata Mahasiswa",
            font=("Arial", 16, "bold")
        )

        self.label_judul.grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )

        # ==============================
        # Nama Lengkap
        # ==============================
        self.label_nama = tk.Label(
            master=self.main_frame,
            text="Nama Lengkap:",
            font=("Arial", 12)
        )

        self.label_nama.grid(
            row=1,
            column=0,
            sticky="W",
            pady=5
        )

        self.entry_nama = tk.Entry(
            master=self.main_frame,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_nama
        )

        self.entry_nama.grid(
            row=1,
            column=1,
            pady=5
        )

        # ==============================
        # NIM
        # ==============================
        self.label_nim = tk.Label(
            master=self.main_frame,
            text="NIM:",
            font=("Arial", 12)
        )

        self.label_nim.grid(
            row=2,
            column=0,
            sticky="W",
            pady=5
        )

        self.entry_nim = tk.Entry(
            master=self.main_frame,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_nim
        )

        self.entry_nim.grid(
            row=2,
            column=1,
            pady=5
        )

        # ==============================
        # Jurusan
        # ==============================
        self.label_jurusan = tk.Label(
            master=self.main_frame,
            text="Jurusan:",
            font=("Arial", 12)
        )

        self.label_jurusan.grid(
            row=3,
            column=0,
            sticky="W",
            pady=5
        )

        self.entry_jurusan = tk.Entry(
            master=self.main_frame,
            width=30,
            font=("Arial", 12),
            textvariable=self.var_jurusan
        )

        self.entry_jurusan.grid(
            row=3,
            column=1,
            pady=5
        )

        # ==============================
        # Jenis Kelamin
        # ==============================
        self.label_jk = tk.Label(
            master=self.main_frame,
            text="Jenis Kelamin:",
            font=("Arial", 12)
        )

        self.label_jk.grid(
            row=4,
            column=0,
            sticky="W",
            pady=5
        )

        # Frame untuk radio button
        self.frame_jk = tk.Frame(
            master=self.main_frame
        )

        self.frame_jk.grid(
            row=4,
            column=1,
            sticky="W"
        )

        # Radio button Pria
        self.radio_pria = tk.Radiobutton(
            master=self.frame_jk,
            text="Pria",
            variable=self.var_jk,
            value="Pria"
        )

        self.radio_pria.pack(
            side=tk.LEFT
        )

        # Radio button Wanita
        self.radio_wanita = tk.Radiobutton(
            master=self.frame_jk,
            text="Wanita",
            variable=self.var_jk,
            value="Wanita"
        )

        self.radio_wanita.pack(
            side=tk.LEFT
        )

        # ==============================
        # Checkbox
        # ==============================
        self.check_setuju = tk.Checkbutton(
            master=self.main_frame,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 10),
            command=self.validate_form
        )

        self.check_setuju.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10,
            sticky="W"
        )

        # ==============================
        # Tombol Submit
        # ==============================
        self.btn_submit = tk.Button(
            master=self.main_frame,
            text="Submit Biodata",
            font=("Arial", 12, "bold"),
            command=self.submit_data,
            state=tk.DISABLED
        )

        self.btn_submit.grid(
            row=6,
            column=0,
            columnspan=2,
            pady=20,
            sticky="EW"
        )

        # ==============================
        # Trace untuk validasi real-time
        # ==============================
        self.var_nama.trace_add(
            "write",
            self.validate_form
        )

        self.var_nim.trace_add(
            "write",
            self.validate_form
        )

        self.var_jurusan.trace_add(
            "write",
            self.validate_form
        )

        # ==============================
        # Event Hover
        # ==============================
        self.btn_submit.bind(
            "<Enter>",
            self.on_enter
        )

        self.btn_submit.bind(
            "<Leave>",
            self.on_leave
        )

        # ==============================
        # Shortcut tombol Enter
        # ==============================
        self.entry_nama.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_nim.bind(
            "<Return>",
            self.submit_shortcut
        )

        self.entry_jurusan.bind(
            "<Return>",
            self.submit_shortcut
        )

        # Warna background
        self.configure(
            bg="#f0f0f0"
        )

    # ==========================================
    # Fungsi Pindah Frame
    # ==========================================
    def _pindah_ke(self, frame):

        # Sembunyikan frame yang sedang aktif
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        # Tampilkan frame baru
        self.frame_aktif = frame

        self.frame_aktif.pack(
            fill=tk.BOTH,
            expand=True
        )

    # ==========================================
    # Fungsi Validasi Form
    # ==========================================
    def validate_form(self, *args):

        nama_valid = self.var_nama.get().strip() != ""
        nim_valid = self.var_nim.get().strip() != ""
        jurusan_valid = self.var_jurusan.get().strip() != ""
        setuju_valid = self.var_setuju.get() == 1

        if (
            nama_valid
            and nim_valid
            and jurusan_valid
            and setuju_valid
        ):
            self.btn_submit.config(
                state=tk.NORMAL
            )

        else:
            self.btn_submit.config(
                state=tk.DISABLED
            )

    # ==========================================
    # Fungsi Submit Data
    # ==========================================
    def submit_data(self):

        # Cek checkbox
        if self.var_setuju.get() == 0:
            messagebox.showwarning(
                "Peringatan",
                "Anda harus menyetujui syarat dan ketentuan."
            )
            return

        # Ambil data dari form
        nama = self.var_nama.get()
        nim = self.var_nim.get()
        jurusan = self.var_jurusan.get()
        jenis_kelamin = self.var_jk.get()

        # Cek field kosong
        if not nama or not nim or not jurusan:
            messagebox.showwarning(
                "Peringatan",
                "Semua field harus diisi."
            )
            return

        # Tampilkan hasil
        hasil = (
            f"Nama: {nama}\n"
            f"NIM: {nim}\n"
            f"Jurusan: {jurusan}\n"
            f"Jenis Kelamin: {jenis_kelamin}"
        )

        messagebox.showinfo(
            "Data Tersimpan",
            hasil
        )

    # ==========================================
    # Fungsi Hover Mouse Masuk
    # ==========================================
    def on_enter(self, event):

        if self.btn_submit["state"] == tk.NORMAL:
            self.btn_submit.config(
                bg="lightblue"
            )

    # ==========================================
    # Fungsi Hover Mouse Keluar
    # ==========================================
    def on_leave(self, event):

        self.btn_submit.config(
            bg="SystemButtonFace"
        )

    # ==========================================
    # Fungsi Shortcut Enter
    # ==========================================
    def submit_shortcut(self, event=None):

        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()


# ==============================================
# Menjalankan Aplikasi
# ==============================================
if __name__ == "__main__":

    app = AplikasiBiodata()

    app.mainloop()