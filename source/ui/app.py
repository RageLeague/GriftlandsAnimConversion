import tkinter as tk
from tkinter import ttk
import webbrowser as wb

from source.ui.anim_editor import AnimEditor
from source.ui.image_editor import ImageEditor

PADDING = 5

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
