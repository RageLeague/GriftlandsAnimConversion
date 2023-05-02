from tkinter.ttk import Treeview
from source.model.anim_project import TreeNode
from typing import Optional

class NodeTreeView(Treeview):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._tracked_id: set[int] = set()
        self.set_base_node(None)

    def set_base_node(self, node: Optional[TreeNode]) -> None:
        self.node = node
        self.update_listing()

    def __update_listing_recurse(self, node: TreeNode, old_tracked: set[int], new_tracked: set[int]) -> str:
        uid = node.get_uid()
        if self.exists(str(uid)):
            new_tracked.add(uid)
            old_tracked.remove(uid)
        else:
            new_tracked.add(uid)
            self.insert('', 'end', text=node.get_node_name(), iid=str(uid))
        for child_node in node.get_children():
            new_id = self.__update_listing_recurse(child_node, old_tracked, new_tracked)
            self.move(new_id, str(uid), len(self.get_children(str(uid))))
        return str(uid)

    def update_listing(self) -> None:
        old_tracked = self._tracked_id.copy()
        new_tracked: set[int] = set()
        # self.detach(*map(str, old_tracked))
        if self.node:
            self.move(self.__update_listing_recurse(self.node, old_tracked, new_tracked), '', 0)
        self.delete(*map(str, old_tracked))
        self._tracked_id = new_tracked
