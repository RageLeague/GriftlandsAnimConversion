import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser as wb
from typing import Optional
from PIL import Image, ImageTk
from source.model.image_format import read_image, write_image
import os, traceback

PADDING = 5

class AnimEditor(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Anim Editor")
        self.minsize(800, 600)

        self.menubar = tk.Menu(self)
        self["menu"] = self.menubar

        fileMenu = tk.Menu(self.menubar)
        fileMenu.add_command(label="Open Animation", command=lambda: None)
        fileMenu.add_command(label="Save", command=lambda: None)

        self.menubar.add_cascade(label="File", menu=fileMenu)

        # Navigate through a project
        # Can navigate through the atlas, builds, and anims
        self.navbar = ttk.Notebook(self)
        self.navbar.pack(side="left", fill="y", padx=PADDING, pady=PADDING)

        # create frames
        frame1 = ttk.Frame(self.navbar, width=200)
        frame2 = ttk.Frame(self.navbar, width=200)

        frame1.pack(fill='both', expand=True)
        frame2.pack(fill='both', expand=True)

        # add frames to notebook

        self.navbar.add(frame1, text='Atlas')
        self.navbar.add(frame2, text='Build')

        ttk.Separator(self, orient="vertical").pack(side="left", fill="y", pady=PADDING)

        self.workspace = tk.Frame(self)
        self.workspace.pack(side="left", fill='both', expand=True)

        self.config_panel = tk.Frame(self.workspace, height=200)
        self.config_panel.pack(side="bottom", fill="x", padx=PADDING, pady=PADDING)

        ttk.Separator(self.workspace, orient="horizontal").pack(side="bottom", fill="x", padx=PADDING)

        self.canvas = tk.Canvas(self.workspace, bg="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING)

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

        image_frame = ttk.Frame(self)
        image_frame.pack(side="top", fill="both", padx=PADDING, pady=PADDING)

        self.display_image: tk.Canvas = tk.Canvas(image_frame)

        h_bar = ttk.Scrollbar(image_frame, orient="horizontal", command=self.display_image.xview)
        h_bar.pack(side="bottom", fill="x")
        v_bar = ttk.Scrollbar(image_frame, orient="vertical", command=self.display_image.yview)
        v_bar.pack(side="right", fill="y")

        self.display_image.configure(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)
        self.display_image.pack(side="top", fill="both", expand=True)

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

        self.display_image.delete("all")
        if self.loaded_photo_image:
            self.display_image.configure(width=self.loaded_photo_image.width(), height=self.loaded_photo_image.height())
            self.display_image.create_image((0, 0), image=self.loaded_photo_image, anchor="nw")
            self.display_image.configure(scrollregion=self.display_image.bbox("all"))
        else:
            self.display_image.configure(width=200, height=100)
            self.display_image.configure(scrollregion=self.display_image.bbox("all"))


    def get_image_info(self) -> str:
        image_name = self.image_name and os.path.basename(self.image_name)
        width, height = self.loaded_image.size if self.loaded_image is not None else (0, 0)
        return f"{image_name} ({width}x{height})"

class App(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.pack()

        frame = ttk.Frame(self, padding=2 * PADDING)
        frame.grid()

        ttk.Label(frame, text="Welcome to Griftlands Animation Explorer!").grid(column=0, row=0, columnspan=3)
        ttk.Button(frame, text="Image Editor", command=lambda: ImageEditor(self.master)).grid(column=0, row=1)
        ttk.Button(frame, text="Anim Editor", command=lambda: AnimEditor(self.master)).grid(column=1, row=1)
        ttk.Button(frame, text="GitHub", command=lambda: wb.open("https://github.com/RageLeague/GriftlandsAnimConversion")).grid(column=2, row=1)

        for widget in frame.winfo_children():
            widget.grid(padx=PADDING, pady=PADDING)


def run():
    root = tk.Tk()
    root.title("Griftlands Animation Explorer")

    App(root)

    root.mainloop()

if __name__ == "__main__":
    run()
