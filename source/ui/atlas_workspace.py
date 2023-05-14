from typing import Optional

from source.model.anim_project import Atlas, AtlasImage
from source.ui.anim_workspace import AnimWorkspace
from source.ui.workspace_controller import WorkspaceController

class AtlasWorkspace(WorkspaceController):
    def __init__(self, root: Optional[Atlas] = None, focus: Atlas | AtlasImage | None = None) -> None:
        self.set_root(root)
        self.set_focus(focus)
        self.__cached_focus: Optional[Atlas] = None

    def update_workspace(self, workspace: AnimWorkspace) -> None:
        if self.root != self.__cached_focus:
            pass # Need to render the image

    def set_root(self, root: Optional[Atlas]):
        self.root = root

    # Focus must be descendent of root, the root itself, or none
    def set_focus(self, focus: Atlas | AtlasImage | None):
        self.focus = focus
