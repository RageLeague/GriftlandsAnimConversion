from dataclasses import dataclass, field
from PIL import Image
from typing import Optional, TypeVar, Protocol, Generator, Any, runtime_checkable
import weakref

@dataclass
class HasUID:
    _uid: int = 0
    _project: Optional['AnimProject'] = None

    def get_uid(self) -> int:
        return self._uid

class TreeNode(Protocol):
    def get_children(self) -> Generator['TreeNode', None, None]:
        ...

    def get_node_name(self) -> str:
        ...

    def get_uid(self) -> int:
        ...

@runtime_checkable
class JsonSavable(Protocol):
    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        ...

@runtime_checkable
class UIDJsonSavable(Protocol):
    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        ...

    def get_uid(self) -> int:
        ...

U = TypeVar("U", bound=HasUID)

@dataclass
class IntCoord:
    x: int = 0
    y: int = 0
    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        return {
            "_type": self.__class__.__name__,
            "x": self.x,
            "y": self.y,
        }

@dataclass
class AtlasImage(HasUID):
    # Reference to the atlas that this image belongs to
    atlas: Optional[weakref.ref['Atlas']] = None
    # Position of top left corner of image within the atlas
    pos: IntCoord = field(default_factory=IntCoord)
    # Optional name for the image to better identify it
    name: str = ""

    def get_children(self) -> Generator['TreeNode', None, None]:
        return
        yield # This is here to make this function a generator lol

    def get_node_name(self) -> str:
        return self.name or f"Image {self.get_uid()}"

    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        atlas = self.atlas and self.atlas()
        result = {
            "_uid": self._uid,
            "_type": self.__class__.__name__,
            "name": self.name,
            "pos": self.pos.save_json(project, obj_dict, asset_dict),
        }
        if atlas:
            result["atlas"] = project.save_json_tracker(atlas.get_uid(), obj_dict, asset_dict)
        return result

@dataclass
class AtlasParent:
    parent: Optional[weakref.ref['Atlas']] = None
    # Position of top left corner of image within the atlas
    pos: IntCoord = field(default_factory=IntCoord)
    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        parent = self.parent and self.parent()
        result = {
            "_type": self.__class__.__name__,
            "pos": self.pos.save_json(project, obj_dict, asset_dict),
        }
        if parent:
            result["parent"] = project.save_json_tracker(parent.get_uid(), obj_dict, asset_dict)
        return result

@dataclass
class Atlas(HasUID):
    parent_info: AtlasParent = field(default_factory=AtlasParent)
    source: Optional[Image.Image] = None
    # Dict of images based on uid
    images: dict[int, AtlasImage] = field(default_factory=dict)
    children: dict[int, 'Atlas'] = field(default_factory=dict)
    # Size of the atlas
    size: IntCoord = field(default_factory=IntCoord)
    # Name for the atlas
    name: str = ""

    def add_image(self, image: AtlasImage) -> AtlasImage:
        if self._project is None:
            raise ValueError("Field _project is None")
        if image.atlas is not None and image.atlas != self:
            raise ValueError("Image already assigned to an atlas")
        self._project.register_object(image)
        obj_id = image.get_uid()
        if obj_id in self.images and self.images[obj_id] != image:
            raise ValueError(f"Image with id {obj_id} already exist")
        self.images[obj_id] = image
        image.atlas = weakref.ref(self)
        return image

    def remove_parent(self) -> None:
        parent = self.parent_info.parent
        parent = parent and parent()
        if parent is not None:
            del parent.children[self.get_uid()]

    def add_child(self, atlas: 'Atlas') -> 'Atlas':
        if self._project is None:
            raise ValueError("Field _project is None")
        self._project.register_object(atlas)
        obj_id = atlas.get_uid()
        if obj_id in self.children and self.children[obj_id] != atlas:
            raise ValueError(f"Atlas with id {obj_id} already exist")
        atlas.remove_parent()
        self.children[obj_id] = atlas
        atlas.parent_info = AtlasParent(weakref.ref(self), IntCoord()) # TODO: Set a better default position
        return atlas

    def get_children(self) -> Generator['TreeNode', None, None]:
        for image_id in self.images:
            yield self.images[image_id]
        for child_id in self.children:
            yield self.children[child_id]

    def get_node_name(self) -> str:
        return self.name or f"Atlas {self.get_uid()}"

    def save_json(self, project: 'AnimProject', obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        result = {
            "_uid": self._uid,
            "_type": self.__class__.__name__,
            "parent_info": self.parent_info.save_json(project, obj_dict, asset_dict),
            "name": self.name,
            "size": self.size.save_json(project, obj_dict, asset_dict),
            "images": [project.save_json_tracker(uid, obj_dict, asset_dict) for uid in self.images],
            "children": [project.save_json_tracker(uid, obj_dict, asset_dict) for uid in self.children]
        }
        if self.source:
            if self.name in asset_dict:
                raise ValueError(f"Image named '{self.name}' appears multiple times")
            asset_dict[self.name] = self.source
        return result

LATEST_PROJECT_VERSION = 1

@dataclass
class AnimProject:
    # Dict of atlases based on uid
    atlas: Atlas = field(default_factory=Atlas)
    objects_by_uid: weakref.WeakValueDictionary[int, HasUID] = field(default_factory=weakref.WeakValueDictionary)

    _current_uid: int = 0
    def get_new_uid(self) -> int:
        self._current_uid += 1
        # Make sure it's not a dupe
        while self._current_uid in self.objects_by_uid:
            self._current_uid += 1
        return self._current_uid

    def register_object(self, obj: U) -> U:
        if obj._project is not None and obj._project != self:
            raise ValueError(f"Object already belongs to another project")
        new_id = obj.get_uid() or self.get_new_uid()
        if new_id in self.objects_by_uid and self.objects_by_uid[new_id] != obj:
            raise ValueError(f"Object with id {new_id} already exist")
        self.objects_by_uid[new_id] = obj
        obj._uid = new_id
        obj._project = self
        return obj

    def save_json_tracker(self, obj_id: int, obj_dict: dict[int, Any], asset_dict: dict[str, Any]) -> Any:
        if obj_id not in obj_dict:
            obj = self.objects_by_uid.get(obj_id)
            if not isinstance(obj, UIDJsonSavable):
                raise ValueError(f"Object not savable")
            obj_id = obj.get_uid()
            obj_dict[obj_id] = {} # This is to mark the object is being saved, so duplicates can be prevented
            obj_dict[obj_id] = obj.save_json(self, obj_dict, asset_dict)
            stored_id = obj_dict[obj_id].get("_uid")
            if stored_id != obj_id:
                raise ValueError(f"Mismatched ID (Expected {obj_id}, but _uid is {stored_id})")
        return {
            "_type": "_Reference",
            "uid_ref": obj_id
        }

    def save_json(self) -> tuple[Any, dict[str, Any]]:
        obj_dict: dict[int, Any] = {}
        asset_dict: dict[str, Any] = {}

        proj = {
            "_version": LATEST_PROJECT_VERSION,
            "atlas": self.save_json_tracker(self.atlas.get_uid(), obj_dict, asset_dict),
            "objects": list(sorted(obj_dict.values(), key=lambda a: a["_uid"]))
        }

        return proj, asset_dict

# Get a project for testing
def get_test_project():
    project = AnimProject()
    project.atlas = project.register_object(Atlas(name="atlas0.tex"))
    project.atlas.add_image(AtlasImage(name="image1"))
    project.atlas.add_image(AtlasImage(name="image2"))
    project.atlas.add_image(AtlasImage(name="image3"))
    sub_atlas = project.atlas.add_child(Atlas(name="atlas1.tex"))
    sub_atlas.add_image(AtlasImage(name="image4"))
    sub_atlas.add_image(AtlasImage(name="image5"))
    return project
