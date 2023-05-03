import tkinter as tk
from tkinter import ttk

from source.model.anim_project import get_test_project
from source.ui.scrollable_canvas import ScrollableCanvas
from source.ui.node_treeview import NodeTreeView
from source.ui.constants import *

class AnimEditor(tk.Toplevel):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.title("Anim Editor")
        self.minsize(800, 600)

        self.loaded_project = get_test_project()

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
        frame_tree = NodeTreeView(frame1)
        frame_tree.set_base_node(self.loaded_project.atlas)
        frame_tree.pack(fill='both', expand=True)

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

        self.work_canvas = ScrollableCanvas(self.workspace)
        self.work_canvas.canvas.configure(bg="white")
        self.work_canvas.resize_scroll()
        self.work_canvas.pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING)
