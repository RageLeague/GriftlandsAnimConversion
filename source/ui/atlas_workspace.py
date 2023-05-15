import tkinter as tk
from tkinter import ttk
from typing import Optional
from PIL import ImageTk

from source.model.anim_project import Atlas, AtlasImage, IntCoord
from source.ui.anim_workspace import AnimWorkspace
from source.ui.workspace_controller import WorkspaceController
from source.ui.constants import *
import source.ui.anim_editor as editor

def set_text(entry: ttk.Entry, s: str) -> None:
    entry.delete(0, tk.END)
    entry.insert(tk.END, s)

class AtlasConfigs(ttk.Frame):
    def __init__(self, atlas: Atlas, workspace: 'AtlasWorkspace', *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.atlas = atlas
        self.workspace = workspace

        ttk.Label(self, text="Pos:").grid(row=0, column=0)
        self.pos_x = ttk.Entry(self, width=INPUT_FIELD_WIDTH, validate="key", validatecommand=self.__field_edited)
        self.pos_x.grid(row=0, column=1)

        self.pos_y = ttk.Entry(self, width=INPUT_FIELD_WIDTH, validate="key", validatecommand=self.__field_edited)
        self.pos_y.grid(row=0, column=2)

        ttk.Button(self, text="Highlight").grid(row=0, column=3)

        ttk.Label(self, text="Size:").grid(row=1, column=0)
        self.size_x = ttk.Entry(self, width=INPUT_FIELD_WIDTH, validate="key", validatecommand=self.__field_edited)
        self.size_x.grid(row=1, column=1)

        self.size_y = ttk.Entry(self, width=INPUT_FIELD_WIDTH, validate="key", validatecommand=self.__field_edited)
        self.size_y.grid(row=1, column=2)

        ttk.Button(self, text="Auto size").grid(row=1, column=3)

        ttk.Button(self, text="Reassign").grid(row=2, column=1)
        ttk.Button(self, text="Import").grid(row=2, column=2)
        ttk.Button(self, text="New Child").grid(row=2, column=3)
        ttk.Button(self, text="Delete").grid(row=2, column=4)

        self.save_button = ttk.Button(self, text="Save", command=self.save_values)
        self.save_button.grid(row=0, column=5)

        self.discard_button = ttk.Button(self, text="Discard", command=self.set_values)
        self.discard_button.grid(row=1, column=5)

        for widget in self.winfo_children():
            widget.grid(padx=PADDING, pady=PADDING)

        self.set_values()

    def __field_edited(self) -> bool:
        self.workspace.mark_dirty()
        return True

    def save_values(self) -> None:
        try:
            self.atlas.parent_info.pos.x = int(self.pos_x.get())
        except ValueError:
            pass
        try:
            self.atlas.parent_info.pos.y = int(self.pos_y.get())
        except ValueError:
            pass
        try:
            self.atlas.size.x = int(self.size_x.get())
        except ValueError:
            pass
        try:
            self.atlas.size.y = int(self.size_y.get())
        except ValueError:
            pass

        self.set_values()

    def set_values(self) -> None:
        set_text(self.pos_x, str(self.atlas.parent_info.pos.x))
        set_text(self.pos_y, str(self.atlas.parent_info.pos.y))
        set_text(self.size_x, str(self.atlas.size.x))
        set_text(self.size_y, str(self.atlas.size.y))

        self.workspace.mark_dirty(False)

    def change_save_highlight(self, enable: bool) -> None:
        self.save_button.configure(state="normal" if enable else "disabled")
        self.discard_button.configure(state="normal" if enable else "disabled")

class AtlasWorkspace(WorkspaceController):
    def __init__(self, root: Optional[Atlas] = None, focus: Atlas | AtlasImage | None = None) -> None:
        self.set_root(root)
        self.set_focus(focus)
        self.__cached_focus: Optional[Atlas] = None
        self.config_panel: AtlasConfigs | None = None

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

        self.config_panel = None
        workspace.reset_config_panel()

        if isinstance(self.focus, Atlas):
            self.config_panel = AtlasConfigs(self.focus, self, workspace.config_panel, padding=PADDING)
            workspace.set_current_name(self.focus.name)
            workspace.set_class_name("Atlas")
            workspace.set_edit_name_fn(lambda s: self.rename_focus(editor, s))
            self.config_panel.grid()
        elif isinstance(self.focus, AtlasImage):
            self.config_panel = None
            workspace.set_current_name(self.focus.name)
            workspace.set_class_name("Image")
            workspace.set_edit_name_fn(lambda s: self.rename_focus(editor, s))
        else:
            self.config_panel = None

        self.mark_dirty(False)

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

    def on_dirty_changed(self) -> None:
        if self.config_panel:
            self.config_panel.change_save_highlight(self.dirty)
