import tkinter as tk
from tkinter import ttk

from source.ui.scrollable_canvas import ScrollableCanvas
from source.ui.constants import *

class AnimWorkspace(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name_bar = tk.Frame(self)
        self.name_bar.pack(side="top", fill="x", pady=PADDING)

        self.current_name = ttk.Label(self.name_bar)
        self.current_name.pack(side="left", padx=PADDING)

        self.edit_name = ttk.Button(self.name_bar, text="Edit", state="disabled")
        self.edit_name.pack(side="left", padx=PADDING)

        self.class_name = ttk.Label(self.name_bar, text="")
        self.class_name.pack(side="right", padx=PADDING)

        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x", padx=PADDING)

        self.config_panel = tk.Frame(self, height=200)
        self.config_panel.pack(side="bottom", fill="x", padx=PADDING, pady=PADDING)

        ttk.Separator(self, orient="horizontal").pack(side="bottom", fill="x", padx=PADDING)

        self.work_canvas = ScrollableCanvas(self)
        self.work_canvas.canvas.configure(bg="white")
        self.work_canvas.resize_scroll()
        self.work_canvas.pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING)

        self.reset_display()

    def set_current_name(self, name: str) -> None:
        self.current_name.configure(text=name)

    def reset_display(self) -> None:
        self.set_current_name("Select an item")
