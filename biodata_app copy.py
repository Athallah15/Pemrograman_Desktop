import tkinter as tk
window = tk.Tk()
window.title("Form Biodata Mahasiswa")
window.geometry("500x600")
window.resizable(True, True)
window.minsize(500, 600)  # Ukuran minimum jendela
 #Membuat frame utama
main_frame = tk.Frame(master=window, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)
main_frame.columnconfigure(1, weight=1)
window.configure(bg="#f0f0f0")
window.mainloop()


