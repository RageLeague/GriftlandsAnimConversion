import tkinter as tk
from typing import Optional
import abc

from source.ui.anim_workspace import AnimWorkspace

class WorkspaceController(abc.ABC):
    def __init__(self) -> None:
        self._dirty = False

    @property
    def dirty(self): return self._dirty

    def mark_dirty(self, dirty: Optional[bool] = None) -> None:
        if dirty is None:
            dirty = True
        self._dirty = dirty

    @abc.abstractmethod
    def update_workspace(self, workspace: AnimWorkspace) -> None:
        ...
