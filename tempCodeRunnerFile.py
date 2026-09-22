     self.title("Aplikasi Biodata Mahasiswa")
            self.geometry("600x700")
            self.resizable(True, True)

            # Atribut untuk manajemen frame
            self.frame_aktif = None

            # Buat tampilan
            self._buat_tampilan_login()
            self._buat_tampilan_biodata()

            # Tampilkan frame login di awal
            self._pindah_ke(self.frame_login)