import datetime
import logging
import re
import tkinter as tk
from tkinter import messagebox

# Setup logging
logging.basicConfig(
    filename="aplikasi_biodata.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class AplikasiBiodata(tk.Tk):

    def simpan_hasil(self):
        """Simpan hasil biodata ke file dengan error handling"""
        try:
            hasil_tersimpan = self.label_hasil.cget("text")

            if not hasil_tersimpan or "BIODATA TERSIMPAN" not in hasil_tersimpan:
                messagebox.showwarning(
                    "Peringatan",
                    "Tidak ada data untuk disimpan. Mohon submit terlebih dahulu.",
                )
                return

            # Buat nama file dengan timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"biodata_{self.current_user}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as file:
                file.write(f"Data disimpan oleh: {self.current_user}\n")
                file.write(
                    f"Waktu penyimpanan: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                )
                file.write("-" * 50 + "\n")
                file.write(hasil_tersimpan)

            messagebox.showinfo(
                "Info", f"Data berhasil disimpan ke file '{filename}'."
            )

        except PermissionError:
            messagebox.showerror(
                "Error",
                "Tidak memiliki izin untuk menyimpan file di lokasi ini.",
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat menyimpan file:\n{str(e)}"
            )

    def __init__(self):
        super().__init__()
        self.title("Login - Sistem Biodata Mahasiswa")
        self.geometry("560x780")
        self.resizable(True, True)

        # Database pengguna sederhana (username: password)
        self.users_db = {
            "admin": "123",
            "user1": "password1",
            "mahasiswa": "123456",
            "Gue Ganteng": "Cihuy123",
        }

        self.current_user = None
        self.saved_username = ""  # Variabel untuk fitur Remember Me
        self.frame_aktif = None

        # Siapkan struktur tampilan
        self._buat_tampilan_login()
        self._buat_tampilan_biodata()

        # Alur awal: kunci akses dan paksa ke halaman login
        self._pindah_ke(self.frame_login)

        # Log aplikasi start
        logging.info("Aplikasi dimulai")

    # ------------------ SISTEM FRAME & NAVIGASI ------------------
    def _pindah_ke(self, frame_tujuan):
        """Menyembunyikan frame sebelumnya dan menampilkan frame target."""
        if self.frame_aktif is not None:
            self.frame_aktif.pack_forget()

        self.frame_aktif = frame_tujuan
        self.frame_aktif.pack(fill=tk.BOTH, expand=True)

        # Fokus otomatis pada input pertama & kelola menu bar
        if frame_tujuan == self.frame_login:
            self._hapus_menu()
            self.after(100, lambda: self.entry_username.focus_set())
        elif frame_tujuan == self.frame_biodata:
            self._buat_menu()
            self.after(100, lambda: self.entry_nama.focus_set())

    def _buat_menu(self):
        """Membuat menu bar untuk aplikasi"""
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(master=menu_bar, tearoff=0)
        file_menu.add_command(label="Simpan Hasil", command=self.simpan_hasil)
        file_menu.add_separator()
        file_menu.add_command(label="Reset Form", command=self._reset_form_biodata)
        file_menu.add_separator()
        file_menu.add_command(label="Logout", command=self._logout)
        file_menu.add_separator()
        file_menu.add_command(label="Keluar", command=self.keluar_aplikasi)

        menu_bar.add_cascade(label="File", menu=file_menu)

    def _hapus_menu(self):
        """Menghapus menu bar saat posisi logout / di halaman login."""
        empty_menu = tk.Menu(self)
        self.config(menu=empty_menu)

    def _update_title(self):
        if self.current_user:
            self.title(
                f"Aplikasi Biodata Mahasiswa — Sesi: {self.current_user}"
            )
        else:
            self.title("Login - Sistem Biodata Mahasiswa")

    # ------------------ HALAMAN 1: LOGIN (GERBANG AWAL) ------------------
    def _buat_tampilan_login(self):
        self.frame_login = tk.Frame(master=self, padx=30, pady=40)
        self.frame_login.grid_columnconfigure(0, weight=0)
        self.frame_login.grid_columnconfigure(1, weight=1)

        # Variabel kontrol Login
        self.var_remember_me = tk.IntVar(value=0)
        self.var_show_pass = tk.IntVar(value=0)

        # Judul Form Login
        tk.Label(
            self.frame_login,
            text="LOGIN SISTEM",
            font=("Arial", 16, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 25))

        # Username Input
        tk.Label(self.frame_login, text="Username:", font=("Arial", 11)).grid(
            row=1, column=0, sticky="W", pady=8
        )
        self.entry_username = tk.Entry(self.frame_login, font=("Arial", 11))
        self.entry_username.grid(row=1, column=1, pady=8, sticky="EW")

        # Password Input
        tk.Label(self.frame_login, text="Password:", font=("Arial", 11)).grid(
            row=2, column=0, sticky="W", pady=8
        )
        self.entry_password = tk.Entry(
            self.frame_login, font=("Arial", 11), show="*"
        )
        self.entry_password.grid(row=2, column=1, pady=8, sticky="EW")

        # Fitur Show/Hide Password & Remember Me
        frame_opts = tk.Frame(self.frame_login)
        frame_opts.grid(row=3, column=0, columnspan=2, sticky="W", pady=5)

        chk_show_pass = tk.Checkbutton(
            frame_opts,
            text="Tampilkan Password",
            variable=self.var_show_pass,
            font=("Arial", 9),
            command=self._toggle_password_visibility,
        )
        chk_show_pass.pack(anchor="w")

        chk_remember = tk.Checkbutton(
            frame_opts,
            text="Ingat Saya (Remember Me)",
            variable=self.var_remember_me,
            font=("Arial", 9),
        )
        chk_remember.pack(anchor="w")

        # Tombol Aksi Login
        self.btn_login = tk.Button(
            self.frame_login,
            text="Masuk",
            font=("Arial", 11, "bold"),
            bg="#2563eb",
            fg="white",
            cursor="hand2",
            command=self._coba_login,
        )
        self.btn_login.grid(
            row=4, column=0, columnspan=2, pady=20, sticky="EW"
        )

        # Shortcut Enter pada login
        self.entry_username.bind(
            "<Return>", lambda e: self.entry_password.focus_set()
        )
        self.entry_password.bind("<Return>", lambda e: self._coba_login())

        # Petunjuk Akun Uji Coba
        info_label = tk.Label(
            self.frame_login,
            text=(
                "Akun tersedia:\n• admin (password: 123)\n• user1 (password: password1)\n"
                "• mahasiswa (password: 123456)\n• Gue Ganteng (password: Cihuy123)"
            ),
            font=("Arial", 9),
            fg="#64748b",
            justify=tk.LEFT,
        )
        info_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="W")

    def _toggle_password_visibility(self):
        """Menampilkan atau menyembunyikan karakter password"""
        if self.var_show_pass.get() == 1:
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def _coba_login(self):
        """Method untuk memproses attempt login dengan logging"""
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        logging.info(f"Login attempt for username: {username}")

        # Validasi input kosong
        if not username or not password:
            logging.warning(
                f"Empty credentials attempt for username: {username}"
            )
            messagebox.showwarning(
                "Login Gagal", "Username dan Password tidak boleh kosong."
            )
            self.entry_username.focus_set()
            return

        # Validasi panjang minimum
        if len(username) < 3:
            logging.warning(f"Username too short: {username}")
            messagebox.showwarning(
                "Login Gagal", "Username minimal 3 karakter."
            )
            self.entry_username.focus_set()
            return

        # Cek kredensial di database
        if username in self.users_db and self.users_db[username] == password:
            self.current_user = username

            # Logika Remember Me
            if self.var_remember_me.get() == 1:
                self.saved_username = username
            else:
                self.saved_username = ""

            logging.info(f"Successful login for user: {username}")
            messagebox.showinfo(
                "Login Berhasil", f"Selamat Datang, {username}!"
            )
            self._reset_form_biodata()
            self._update_title()
            self._pindah_ke(self.frame_biodata)

            # Bersihkan password field
            self.entry_password.delete(0, tk.END)
        else:
            logging.warning(f"Failed login attempt for username: {username}")
            messagebox.showerror(
                "Login Gagal", "Username atau Password salah."
            )
            self.entry_password.delete(0, tk.END)
            self.entry_username.focus_set()

    def _logout(self):
        """Method untuk logout dengan logging"""
        if messagebox.askyesno(
            "Logout", f"Apakah {self.current_user} yakin ingin logout?"
        ):
            logging.info(f"User logout: {self.current_user}")
            self.current_user = None
            self._update_title()

            # Reset form & password
            self.entry_password.delete(0, tk.END)
            self.entry_username.delete(0, tk.END)

            # Jika Remember Me aktif, isi ulang username
            if self.saved_username:
                self.entry_username.insert(0, self.saved_username)
                self.var_remember_me.set(1)

            self._reset_form_biodata()
            self._pindah_ke(self.frame_login)

    # ------------------ HALAMAN 2: FORM BIODATA (SETELAH LOGIN) ------------------
    def _buat_tampilan_biodata(self):
        self.frame_biodata = tk.Frame(master=self, padx=20, pady=10)

        # Variabel kontrol data
        self.var_nama = tk.StringVar()
        self.var_nim = tk.StringVar()
        self.var_jurusan = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_telepon = tk.StringVar()
        self.var_tgl_lahir = tk.StringVar()
        self.var_jk = tk.StringVar(value="Pria")
        self.var_setuju = tk.IntVar(value=0)

        # Tracing untuk validasi tombol submit secara real-time
        self.var_nama.trace_add("write", self.validate_form)
        self.var_nim.trace_add("write", self.validate_form)
        self.var_jurusan.trace_add("write", self.validate_form)
        self.var_email.trace_add("write", self.validate_form)
        self.var_telepon.trace_add("write", self.validate_form)
        self.var_tgl_lahir.trace_add("write", self.validate_form)

        # Header Form
        label_judul = tk.Label(
            master=self.frame_biodata,
            text="FORM BIODATA MAHASISWA",
            font=("Arial", 15, "bold"),
        )
        label_judul.pack(pady=10)

        # Container Input
        frame_input = tk.Frame(
            master=self.frame_biodata,
            relief=tk.GROOVE,
            borderwidth=2,
            padx=15,
            pady=12,
        )
        frame_input.pack(fill=tk.X, expand=False)
        frame_input.columnconfigure(1, weight=1)

        # Nama
        tk.Label(frame_input, text="Nama Lengkap:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="W", pady=4
        )
        self.entry_nama = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nama
        )
        self.entry_nama.grid(row=0, column=1, sticky="EW", pady=4)

        # NIM
        tk.Label(frame_input, text="NIM:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="W", pady=4
        )
        self.entry_nim = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_nim
        )
        self.entry_nim.grid(row=1, column=1, sticky="EW", pady=4)

        # Jurusan
        tk.Label(frame_input, text="Jurusan:", font=("Arial", 10)).grid(
            row=2, column=0, sticky="W", pady=4
        )
        self.entry_jurusan = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_jurusan
        )
        self.entry_jurusan.grid(row=2, column=1, sticky="EW", pady=4)

        # Email (Validasi Lanjutan)
        tk.Label(frame_input, text="Email:", font=("Arial", 10)).grid(
            row=3, column=0, sticky="W", pady=4
        )
        self.entry_email = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_email
        )
        self.entry_email.grid(row=3, column=1, sticky="EW", pady=4)

        # Nomor Telepon (Validasi Lanjutan)
        tk.Label(frame_input, text="No. Telepon:", font=("Arial", 10)).grid(
            row=4, column=0, sticky="W", pady=4
        )
        self.entry_telepon = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_telepon
        )
        self.entry_telepon.grid(row=4, column=1, sticky="EW", pady=4)

        # Tanggal Lahir (Validasi Lanjutan)
        tk.Label(
            frame_input, text="Tgl Lahir (YYYY-MM-DD):", font=("Arial", 10)
        ).grid(row=5, column=0, sticky="W", pady=4)
        self.entry_tgl_lahir = tk.Entry(
            frame_input, font=("Arial", 10), textvariable=self.var_tgl_lahir
        )
        self.entry_tgl_lahir.grid(row=5, column=1, sticky="EW", pady=4)

        # Alamat (Text Area + Scrollbar)
        tk.Label(frame_input, text="Alamat:", font=("Arial", 10)).grid(
            row=6, column=0, sticky="NW", pady=4
        )
        frame_alamat = tk.Frame(frame_input, relief=tk.SUNKEN, borderwidth=1)
        frame_alamat.grid(row=6, column=1, sticky="EW", pady=4)

        scrollbar_alamat = tk.Scrollbar(frame_alamat)
        scrollbar_alamat.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_alamat = tk.Text(
            frame_alamat,
            height=3,
            font=("Arial", 10),
            yscrollcommand=scrollbar_alamat.set,
        )
        self.text_alamat.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_alamat.config(command=self.text_alamat.yview)

        # Jenis Kelamin
        tk.Label(frame_input, text="Jenis Kelamin:", font=("Arial", 10)).grid(
            row=7, column=0, sticky="W", pady=4
        )
        frame_jk = tk.Frame(frame_input)
        frame_jk.grid(row=7, column=1, sticky="W", pady=4)

        tk.Radiobutton(
            frame_jk, text="Pria", variable=self.var_jk, value="Pria"
        ).pack(side=tk.LEFT, padx=(0, 15))
        tk.Radiobutton(
            frame_jk, text="Wanita", variable=self.var_jk, value="Wanita"
        ).pack(side=tk.LEFT)

        # Checkbox Persetujuan
        check_setuju = tk.Checkbutton(
            frame_input,
            text="Saya menyetujui pengumpulan data ini.",
            variable=self.var_setuju,
            font=("Arial", 9),
            command=self.validate_form,
        )
        check_setuju.grid(row=8, column=0, columnspan=2, sticky="W", pady=8)

        # Tombol Aksi (Submit & Reset)
        frame_tombol = tk.Frame(self.frame_biodata)
        frame_tombol.pack(fill=tk.X, pady=10)

        self.btn_submit = tk.Button(
            frame_tombol,
            text="Simpan Data Biodata",
            font=("Arial", 11, "bold"),
            bg="#16a34a",
            fg="white",
            command=self.submit_data,
            state=tk.DISABLED,
        )
        self.btn_submit.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        self.btn_reset = tk.Button(
            frame_tombol,
            text="Reset Form",
            font=("Arial", 11, "bold"),
            bg="#dc2626",
            fg="white",
            command=self._reset_form_biodata,
        )
        self.btn_reset.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        # Preview Data Tersimpan
        self.label_hasil = tk.Label(
            self.frame_biodata,
            text="",
            font=("Arial", 10),
            justify=tk.LEFT,
            fg="#1e293b",
        )
        self.label_hasil.pack(anchor="w", padx=5, pady=5)

    # ------------------ LOGIKA VALIDASI & AKSI BIODATA ------------------
    def validate_form(self, *args):
        """Tombol submit hanya aktif jika seluruh field wajib telah diisi."""
        nama_ada = self.var_nama.get().strip() != ""
        nim_ada = self.var_nim.get().strip() != ""
        jurusan_ada = self.var_jurusan.get().strip() != ""
        email_ada = self.var_email.get().strip() != ""
        telepon_ada = self.var_telepon.get().strip() != ""
        tgl_lahir_ada = self.var_tgl_lahir.get().strip() != ""
        setuju = self.var_setuju.get() == 1

        if (
            nama_ada
            and nim_ada
            and jurusan_ada
            and email_ada
            and telepon_ada
            and tgl_lahir_ada
            and setuju
        ):
            self.btn_submit.config(state=tk.NORMAL)
        else:
            self.btn_submit.config(state=tk.DISABLED)

    def submit_shortcut(self, event=None):
        if self.btn_submit["state"] == tk.NORMAL:
            self.submit_data()

    def submit_data(self):
        """Submit data biodata dengan validasi lengkap dan lanjutan"""
        try:
            # 1. Cek persetujuan checkbox
            if self.var_setuju.get() == 0:
                messagebox.showwarning(
                    "Peringatan", "Anda harus menyetujui pengumpulan data!"
                )
                return

            # 2. Ambil data dari form
            nama = self.entry_nama.get().strip()
            nim = self.entry_nim.get().strip()
            jurusan = self.entry_jurusan.get().strip()
            email = self.entry_email.get().strip()
            telepon = self.entry_telepon.get().strip()
            tgl_lahir = self.entry_tgl_lahir.get().strip()
            alamat = self.text_alamat.get("1.0", tk.END).strip()
            jenis_kelamin = self.var_jk.get()

            # 3. Validasi field kosong
            if not nama or not nim or not jurusan or not email or not telepon or not tgl_lahir:
                messagebox.showwarning(
                    "Input Kosong", "Seluruh field formulir harus diisi!"
                )
                return

            if not alamat:
                messagebox.showwarning("Input Kosong", "Field alamat belum diisi.")
                self.text_alamat.focus_set()
                return

            # 4. Validasi format NIM (harus angka dan minimal 8 digit)
            if not nim.isdigit() or len(nim) < 8:
                messagebox.showwarning(
                    "Format NIM Salah",
                    "NIM harus berupa angka minimal 8 digit!",
                )
                self.entry_nim.focus_set()
                return

            # 5. Validasi nama (tidak boleh hanya angka)
            if nama.isdigit():
                messagebox.showwarning(
                    "Format Nama Salah", "Nama tidak boleh hanya berupa angka!"
                )
                self.entry_nama.focus_set()
                return

            # 6. Validasi Format Email
            email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(email_pattern, email):
                messagebox.showwarning(
                    "Format Email Salah",
                    "Masukkan format email yang valid (contoh: nama@domain.com)!",
                )
                self.entry_email.focus_set()
                return

            # 7. Validasi Format Telepon Indonesia
            # Harus diawali '08' atau '+628' dan terdiri dari 10-14 digit
            phone_pattern = r"^(08|\+628)[0-9]{8,11}$"
            if not re.match(phone_pattern, telepon):
                messagebox.showwarning(
                    "Format Telepon Salah",
                    "Nomor telepon harus format Indonesia (diawali '08' atau '+628' dengan total 10-14 digit)!",
                )
                self.entry_telepon.focus_set()
                return

            # 8. Validasi Tanggal Lahir (YYYY-MM-DD)
            try:
                datetime.datetime.strptime(tgl_lahir, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning(
                    "Format Tanggal Salah",
                    "Format tanggal lahir harus YYYY-MM-DD (contoh: 2002-08-17)!",
                )
                self.entry_tgl_lahir.focus_set()
                return

            # 9. Format dan tampilkan hasil
            hasil = (
                f"Nama: {nama}\n"
                f"NIM: {nim}\n"
                f"Jurusan: {jurusan}\n"
                f"Email: {email}\n"
                f"Telepon: {telepon}\n"
                f"Tanggal Lahir: {tgl_lahir}\n"
                f"Jenis Kelamin: {jenis_kelamin}\n"
                f"Alamat: {alamat}"
            )

            messagebox.showinfo("Data Tersimpan", hasil)

            # Tampilkan hasil di label dengan info user
            hasil_lengkap = (
                f"BIODATA TERSIMPAN:\nDiinput oleh: {self.current_user}\n\n{hasil}"
            )
            self.label_hasil.config(text=hasil_lengkap)

            # Log successful data submission
            logging.info(
                f"Data submitted by user: {self.current_user} - NIM: {nim}"
            )

        except Exception as e:
            logging.error(
                f"Error in submit_data by {self.current_user}: {str(e)}"
            )
            messagebox.showerror(
                "Error", f"Terjadi kesalahan saat memproses data:\n{str(e)}"
            )

    def _reset_form_biodata(self):
        """Mengosongkan isian formulir."""
        self.var_nama.set("")
        self.var_nim.set("")
        self.var_jurusan.set("")
        self.var_email.set("")
        self.var_telepon.set("")
        self.var_tgl_lahir.set("")
        self.text_alamat.delete("1.0", tk.END)
        self.var_jk.set("Pria")
        self.var_setuju.set(0)
        self.label_hasil.config(text="")
        self.btn_submit.config(state=tk.DISABLED)

    def keluar_aplikasi(self):
        """Keluar dari aplikasi dengan konfirmasi"""
        if messagebox.askokcancel(
            "Keluar", "Apakah Anda yakin ingin keluar dari aplikasi?"
        ):
            logging.info(f"Application closed by user: {self.current_user}")
            self.destroy()


if __name__ == "__main__":
    app = AplikasiBiodata()
    app.mainloop()