import tkinter as tk
from tkinter import ttk
from typing import Optional
from PIL import ImageTk

from source.model.anim_project import Atlas, AtlasImage, IntCoord
from source.ui.anim_workspace import AnimWorkspace
from source.ui.workspace_controller import WorkspaceController
from source.ui.constants import *
import source.ui.anim_editor as editor

class AtlasConfigs(ttk.Frame):
    def __init__(self, atlas: Atlas, workspace: 'AtlasWorkspace', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.atlas = atlas
        self.workspace = workspace
        ttk.Label(self, text="Pos:").grid(row=0, column=0)
        self.pos_x = tk.Text(self, height=1, width=10)
        self.pos_x.insert(tk.END, str(atlas.parent_info.pos.x))
        self.pos_x.grid(row=0, column=1)

        self.pos_y = tk.Text(self, height=1, width=10)
        self.pos_y.insert(tk.END, str(atlas.parent_info.pos.y))
        self.pos_y.grid(row=0, column=2)

        ttk.Label(self, text="Size:").grid(row=1, column=0)
        self.size_x = tk.Text(self, height=1, width=10)
        self.size_x.insert(tk.END, str(atlas.size.x))
        self.size_x.grid(row=1, column=1)

        self.size_y = tk.Text(self, height=1, width=10)
        self.size_y.insert(tk.END, str(atlas.size.y))
        self.size_y.grid(row=1, column=2)

        for widget in self.winfo_children():
            widget.grid(padx=PADDING, pady=PADDING)

class AtlasWorkspace(WorkspaceController):
    def __init__(self, root: Optional[Atlas] = None, focus: Atlas | AtlasImage | None = None) -> None:
        self.set_root(root)
        self.set_focus(focus)
        self.__cached_focus: Optional[Atlas] = None

    def render_atlas(self, canvas: tk.Canvas, loaded_images: list[ImageTk.PhotoImage], atlas: Atlas, offset: IntCoord) -> None:
        pos = atlas.parent_info.pos or IntCoord()
        offset = offset + pos
        if atlas.source:
            loaded_image = ImageTk.PhotoImage(atlas.source)
            canvas.create_image(offset.to_tuple(), image=loaded_image, anchor="nw")
            loaded_images.append(loaded_image)
        for child in atlas.children.values():
            self.render_atlas(canvas, loaded_images, child, offset)

    def update_workspace(self, workspace: AnimWorkspace, editor: 'editor.AnimEditor') -> None:
        if self.root != self.__cached_focus:
            workspace.work_canvas.canvas.delete("all")
            self.loaded_images: list[ImageTk.PhotoImage] = []
            if self.root:
                self.render_atlas(workspace.work_canvas.canvas, self.loaded_images, self.root, IntCoord())

        workspace.reset_config_panel()

        self.mark_dirty(False)

        if isinstance(self.focus, Atlas):
            self.config_panel = AtlasConfigs(self.focus, self, workspace.config_panel, padding=PADDING)
            workspace.set_current_name(self.focus.name)
            workspace.set_class_name("Atlas")
            workspace.set_edit_name_fn(lambda s: self.rename_focus(editor, s))
            self.config_panel.grid()
        elif isinstance(self.focus, AtlasImage):
            workspace.set_current_name(self.focus.name)
            workspace.set_class_name("Image")
            workspace.set_edit_name_fn(lambda s: self.rename_focus(editor, s))

    def rename_focus(self, editor: 'editor.AnimEditor', newname: str):
        if isinstance(self.focus, Atlas):
            self.focus.name = newname
            if self.focus.project:
                self.focus.project.mark_dirty()
            editor.refresh_screen()
        elif isinstance(self.focus, AtlasImage):
            self.focus.name = newname
            if self.focus.project:
                self.focus.project.mark_dirty()
            editor.refresh_screen()

    def set_root(self, root: Optional[Atlas]):
        self.root = root

    # Focus must be descendent of root, the root itself, or none
    def set_focus(self, focus: Atlas | AtlasImage | None):
        self.focus = focus
