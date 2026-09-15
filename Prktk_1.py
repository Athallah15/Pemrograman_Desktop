import tkinter as tk
from tkinter import ttk

root = tk.Tk()
style = ttk.Style()

print(style.theme_names())

style.theme_use('clam')

style.configure("custom.TButton",
        padding=6,
        relief="flat",
        background="#4caf50",
        foreground="white")

style.map("custom.TButton",
        background=[("active", "#45a049"), ("disabled", "#888")])

btn = ttk.Button(root, text="styled Button", style="custom.TButton")
btn.pack(pady=20)

root.mainloop()

