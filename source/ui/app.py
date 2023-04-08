import tkinter as tk
from tkinter import ttk
import webbrowser as wb
from typing import Optional
from PIL import Image, ImageTk

class AnimEditor(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar

        fileMenu = tk.Menu(self.menubar)
        fileMenu.add_command(label="Open Animation", command=lambda: None)
        fileMenu.add_command(label="Save", command=lambda: None)

        self.menubar.add_cascade(label="File", menu=fileMenu)

class ImageEditor(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Image Editor")

        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar

        fileMenu = tk.Menu(self.menubar)
        fileMenu.add_command(label="Open", command=lambda: None)
        fileMenu.add_command(label="Save", command=lambda: None)
        fileMenu.add_command(label="Save As", command=lambda: None)

        self.menubar.add_cascade(label="File", menu=fileMenu)

        self.frame = ttk.Frame(self, padding=10)
        self.frame.grid()

        self.image_info: ttk.Label = ttk.Label(self.frame)
        self.image_info.grid(column=0, row=0)

        ttk.Separator(self.frame, orient="horizontal").grid(column=0, row=1, sticky="ew")

        self.display_image: ttk.Label = ttk.Label(self.frame)
        self.display_image.grid(column=0, row=2)

        self.update_image(Image.new("RGBA", (600, 800), "purple"))

        for widget in self.frame.winfo_children():
            widget.grid(padx=5, pady=5)

    def update_image(self, image: Optional[Image.Image], image_name: Optional[str] = None) -> None:
        self.image_name = image_name
        self.loaded_image = image
        self.loaded_photo_image: Optional[ImageTk.PhotoImage] = ImageTk.PhotoImage(self.loaded_image)
        self.image_info.configure(text=self.get_image_info())
        self.display_image.configure(image=self.loaded_photo_image)

    def get_image_info(self) -> str:
        image_name = self.image_name
        width, height = self.loaded_image.size if self.loaded_image is not None else (0, 0)
        return f"{image_name} ({width}x{height})"

class App(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.pack()

        frame = ttk.Frame(self, padding=10)
        frame.grid()

        ttk.Label(frame, text="Welcome to Griftlands Animation Explorer!").grid(column=0, row=0, columnspan=3)
        ttk.Button(frame, text="Image Editor", command=lambda: ImageEditor(self.master)).grid(column=0, row=1)
        ttk.Button(frame, text="Anim Editor", command=lambda: AnimEditor(self.master)).grid(column=1, row=1)
        ttk.Button(frame, text="GitHub", command=lambda: wb.open("https://github.com/RageLeague/GriftlandsAnimConversion")).grid(column=2, row=1)

        for widget in frame.winfo_children():
            widget.grid(padx=5, pady=5)


def run():
    root = tk.Tk()
    root.title("Griftlands Animation Explorer")

    App(root)

    root.mainloop()

if __name__ == "__main__":
    run()
