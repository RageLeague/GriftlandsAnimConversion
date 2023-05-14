import tkinter as tk
from typing import Optional
import abc

from source.ui.anim_workspace import AnimWorkspace
import source.ui.anim_editor as editor

class WorkspaceController(abc.ABC):
    def __init__(self) -> None:
        self._dirty = False

    @property
    def dirty(self): return self._dirty

    def mark_dirty(self, dirty: Optional[bool] = None) -> None:
        if dirty is None:
            dirty = True
        self._dirty = dirty
        self.on_dirty_changed()

    def on_dirty_changed(self) -> None:
        pass

    @abc.abstractmethod
    def update_workspace(self, workspace: AnimWorkspace, editor: 'editor.AnimEditor') -> None:
        ...
