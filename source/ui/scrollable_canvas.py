import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class ScrollableCanvas(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.canvas: tk.Canvas = tk.Canvas(self)

        h_bar = ttk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)
        h_bar.pack(side="bottom", fill="x")
        v_bar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        v_bar.pack(side="right", fill="y")

        self.canvas.configure(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)
        self.canvas.pack(side="top", fill="both", expand=True)
