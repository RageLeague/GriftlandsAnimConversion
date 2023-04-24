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

        self.canvas_padding = 0

    def set_size(self, width: int, height: int) -> None:
        self.canvas.configure(width=width, height=height)

    def resize_scroll(self) -> None:
        bbox = self.canvas.bbox("all")
        if bbox:
            x1, y1, x2, y2 = bbox
            self.canvas.configure(scrollregion=(x1 - self.canvas_padding, y1 - self.canvas_padding, x2 + self.canvas_padding, y2 + self.canvas_padding))
        else:
            self.canvas.configure(scrollregion=bbox)
