import tkinter as tk
from tkinter import ttk
from typing import Optional

from source.model.anim_project import Atlas, AtlasImage, get_test_project
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

        self.__create_atlas_tab()
        self.__create_build_tab()

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

    def __create_atlas_tab(self) -> None:
        # create frames
        self.atlas_bar = ttk.Frame(self.navbar, width=200)

        self.atlas_tree = NodeTreeView(self.atlas_bar)
        self.atlas_tree.heading("#0", text="Atlas", anchor="w")
        self.atlas_tree.set_base_node(self.loaded_project.atlas)

        self.atlas_tree.pack(fill='both', expand=True)
        self.atlas_tree.bind("<Double-1>", self.__on_atlas_entry_double_click)

        self.atlas_bar.pack(fill='both', expand=True)

        # add frames to notebook
        self.navbar.add(self.atlas_bar, text="Atlas")

    def __create_build_tab(self) -> None:
        self.build_bar = ttk.Frame(self.navbar, width=200)
        self.build_bar.pack(fill='both', expand=True)

        # add frames to notebook
        self.navbar.add(self.build_bar, text="Build")

    def __get_selected_entry(self) -> Optional[str]:
        selection = self.atlas_tree.selection()
        if selection:
            return selection[0]
        return None

    def __on_atlas_entry_select(self, selected_item: int) -> None:
        print(f"Selected entry: {selected_item}")
        item = self.loaded_project.objects_by_uid.get(selected_item)
        if isinstance(item, Atlas):
            item.add_image(AtlasImage())
            self.atlas_tree.update_listing()
            self.atlas_tree.focus(str(item.get_uid()))
            self.atlas_tree.item(str(item.get_uid()), open=False)

    def __on_atlas_entry_double_click(self, event: tk.Event) -> None:
        e = event.widget                                  # Get event controls
        iid: str = e.identify("item",event.x,event.y)
        if iid.isdigit():
            self.__on_atlas_entry_select(int(iid))
