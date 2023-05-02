import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from PIL import Image, ImageTk
import os, traceback

from source.model.image_format import read_image, write_image
from source.ui.scrollable_canvas import ScrollableCanvas
from source.ui.constants import *

class ImageEditor(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Image Editor")
        self.minsize(200, 100)

        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar

        fileMenu = tk.Menu(self.menubar)
        fileMenu.add_command(label="Open", command=self.open_image)
        fileMenu.add_command(label="Save", command=self.save_image)

        self.menubar.add_cascade(label="File", menu=fileMenu)

        self.image_info: ttk.Label = ttk.Label(self, anchor="n")
        self.image_info.pack(side="top", fill="x", padx=PADDING, pady=PADDING)

        ttk.Separator(self, orient="horizontal").pack(side="top", fill="x", padx=PADDING)

        self.image = ScrollableCanvas(self)

        self.image.pack(side="top", fill="both", padx=PADDING, pady=PADDING)

        self.update_image(None) # Image.new("RGBA", (600, 800), "purple")

    def open_image(self) -> None:
        try:
            filename = filedialog.askopenfilename(filetypes=[("Any Image File", [".png", ".tex", ".dds"]), ("PNG File", ".png"), ("Klei Tex File", ".tex"), ("DDS File", ".dds")], initialdir=self.image_name and os.path.dirname(self.image_name))
            # print(filename)
            if filename:
                self.update_image(read_image(filename), filename)
        except Exception as e:
            traceback.print_exception(e)
            messagebox.showerror("Error while reading file", f"{type(e).__name__}: {e}")

    def save_image(self) -> None:
        if self.loaded_image is None:
            return
        try:
            filename = filedialog.asksaveasfilename(filetypes=[("Any Image File", [".png", ".tex", ".dds"]), ("PNG File", ".png"), ("Klei Tex File", ".tex"), ("DDS File", ".dds")], initialfile=self.image_name and os.path.basename(self.image_name))
            # print(filename)
            if filename:
                write_image(filename, self.loaded_image)
        except Exception as e:
            traceback.print_exception(e)
            messagebox.showerror("Error while writing file", f"{type(e).__name__}: {e}")


    def update_image(self, image: Optional[Image.Image], image_name: Optional[str] = None) -> None:
        self.image_name = image_name
        self.loaded_image = image
        self.loaded_photo_image: Optional[ImageTk.PhotoImage] = self.loaded_image and ImageTk.PhotoImage(self.loaded_image)
        self.image_info.configure(text=self.get_image_info())

        self.image.canvas.delete("all")
        if self.loaded_photo_image:
            self.image.set_size(self.loaded_photo_image.width(), self.loaded_photo_image.height())
            self.image.canvas.create_image((0, 0), image=self.loaded_photo_image, anchor="nw")
            self.image.resize_scroll()
        else:
            self.image.set_size(200, 100)
            self.image.resize_scroll()


    def get_image_info(self) -> str:
        image_name = self.image_name and os.path.basename(self.image_name)
        width, height = self.loaded_image.size if self.loaded_image is not None else (0, 0)
        return f"{image_name} ({width}x{height})"
