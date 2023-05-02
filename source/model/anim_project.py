from dataclasses import dataclass, field
from PIL import Image
from typing import Optional, TypeVar, Protocol, Generator
import weakref

@dataclass
class IntCoord:
    x: int = 0
    y: int = 0

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

U = TypeVar("U", bound=HasUID)

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
        return self.name or "Image"

@dataclass
class AtlasParent:
    parent: Optional[weakref.ref['Atlas']] = None
    # Position of top left corner of image within the atlas
    pos: IntCoord = field(default_factory=IntCoord)

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
        obj_id = image._uid
        if obj_id in self.images and self.images[obj_id] != image:
            raise ValueError(f"Image with id {obj_id} already exist")
        self.images[obj_id] = image
        image.atlas = weakref.ref(self)
        return image

    def remove_parent(self) -> None:
        parent = self.parent_info.parent
        parent = parent and parent()
        if parent is not None:
            del parent.children[self._uid]

    def add_child(self, atlas: 'Atlas') -> 'Atlas':
        if self._project is None:
            raise ValueError("Field _project is None")
        self._project.register_object(atlas)
        obj_id = atlas._uid
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
        return self.name or "Atlas"

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
        new_id = obj._uid or self.get_new_uid()
        if new_id in self.objects_by_uid and self.objects_by_uid[new_id] != obj:
            raise ValueError(f"Object with id {new_id} already exist")
        self.objects_by_uid[new_id] = obj
        obj._uid = new_id
        obj._project = self
        return obj

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
