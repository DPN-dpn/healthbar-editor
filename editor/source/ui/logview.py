import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class LogView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.log_text = ScrolledText(self, height=6, state="disabled", font=("Consolas", 10))
        self.log_text.pack(fill=tk.BOTH, expand=True)

    def append_log(self, msg):
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{now}] {msg}"
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_line + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
