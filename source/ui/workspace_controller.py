import tkinter as tk
import abc
from source.ui.anim_workspace import AnimWorkspace

class WorkspaceController(abc.ABC):
    @abc.abstractmethod
    def update_workspace(self, canvas: AnimWorkspace):
        ...
