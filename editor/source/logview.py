import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class LogView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=10)
        self.log_text = ScrolledText(self, height=6, state="disabled", font=("Consolas", 10))
        self.log_text.pack(fill=tk.X)

    def append_log(self, msg):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
