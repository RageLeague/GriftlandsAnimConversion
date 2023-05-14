import tkinter as tk
from tkinter import _Cursor, _Relief, _ScreenUnits, _TakeFocusValue, Misc
from typing import Any, Optional
from typing_extensions import Literal
from PIL import ImageTk

from source.model.anim_project import Atlas, AtlasImage, IntCoord
from source.ui.anim_workspace import AnimWorkspace
from source.ui.workspace_controller import WorkspaceController

class AtlasConfigs(tk.Frame):
    def __init__(self, atlas: Atlas, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.atlas = atlas

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

    def update_workspace(self, workspace: AnimWorkspace) -> None:
        if self.root != self.__cached_focus:
            workspace.work_canvas.canvas.delete("all")
            self.loaded_images: list[ImageTk.PhotoImage] = []
            if self.root:
                self.render_atlas(workspace.work_canvas.canvas, self.loaded_images, self.root, IntCoord())

        workspace.reset_config_panel()

        self.mark_dirty(False)

        if isinstance(self.focus, Atlas):
            pass # Render the config panel for an atlas
        elif isinstance(self.focus, AtlasImage):
            pass # Render the config panel for an atlas image

    def set_root(self, root: Optional[Atlas]):
        self.root = root

    # Focus must be descendent of root, the root itself, or none
    def set_focus(self, focus: Atlas | AtlasImage | None):
        self.focus = focus
