import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser as wb
import traceback

from source.model.anim_project import get_test_project
from source.model.anim_project_io import load_project
from source.ui.anim_editor import AnimEditor
from source.ui.image_editor import ImageEditor

PADDING = 5

class App(tk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__( *args, **kwargs)
        self.pack()

        frame = ttk.Frame(self, padding=2 * PADDING)
        frame.grid()

        ttk.Label(frame, text="Welcome to Griftlands Animation Explorer!").grid(column=0, row=0, columnspan=4)
        ttk.Button(frame, text="Image Editor", command=lambda: ImageEditor(self.master)).grid(column=0, row=1)
        ttk.Button(frame, text="Anim Editor (New)", command=lambda: AnimEditor(get_test_project(), self.master)).grid(column=1, row=1)
        ttk.Button(frame, text="Anim Editor (Open)", command=self.open_project).grid(column=2, row=1)
        ttk.Button(frame, text="GitHub", command=lambda: wb.open("https://github.com/RageLeague/GriftlandsAnimConversion")).grid(column=3, row=1)

        for widget in frame.winfo_children():
            widget.grid(padx=PADDING, pady=PADDING)

    def open_project(self) -> None:
        try:
            filename = filedialog.askopenfilename(filetypes=[("Project File", ".json")])
            # print(filename)
            if filename:
                AnimEditor(load_project(filename), self.master)
        except Exception as e:
            traceback.print_exception(e)
            messagebox.showerror("Error while reading file", f"{type(e).__name__}: {e}")
def run():
    root = tk.Tk()
    root.title("Griftlands Animation Explorer")

    App(root)

    root.mainloop()

if __name__ == "__main__":
    run()
