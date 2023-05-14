import tkinter as tk
from tkinter import ttk, simpledialog
from typing import Callable, Optional, Any

from source.ui.scrollable_canvas import ScrollableCanvas
from source.ui.constants import *

class AnimWorkspace(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.name_bar = tk.Frame(self)
        self.name_bar.pack(side="top", fill="x", pady=PADDING)

        self.current_name = ttk.Label(self.name_bar)
        self.current_name.pack(side="left", padx=PADDING)

        self.edit_name = ttk.Button(self.name_bar, text="Edit", state="disabled", command=self.__ask_edit_name)
        self.edit_name.pack(side="left", padx=PADDING)

        self.class_name = ttk.Label(self.name_bar)
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

    def set_current_name(self, name: str, default_name: Optional[str] = None) -> None:
        self.current_name.configure(text=name)
        if default_name is None:
            default_name = name
        self.default_name = default_name

    def set_class_name(self, name: str) -> None:
        self.class_name.configure(text=name)

    def set_edit_name_fn(self, fn: Optional[Callable[[str], Any]]) -> None:
        self.edit_fn = fn
        if fn:
            self.edit_name.configure(state="normal")
        else:
            self.edit_name.configure(state="disabled")

    def __ask_edit_name(self) -> None:
        res = simpledialog.askstring("Rename", "Please enter a new name for this object...", initialvalue=self.default_name)
        if res is not None and self.edit_fn:
            self.edit_fn(res)

    def reset_names(self) -> None:
        self.set_current_name("Select an item")
        self.set_class_name("")
        self.set_edit_name_fn(None)

    def reset_canvas(self) -> None:
        self.work_canvas.canvas.delete("all")

    def reset_config_panel(self) -> None:
        for child in self.config_panel.winfo_children():
            child.destroy()

    def reset_display(self) -> None:
        self.reset_names()
        self.reset_canvas()
        self.reset_config_panel()
