from dataclasses import dataclass, field
from PIL import Image
from typing import Optional, TypeVar

@dataclass
class IntCoord:
    x: int = 0
    y: int = 0

@dataclass
class HasUID:
    _uid: int = 0

U = TypeVar("U", bound=HasUID)

@dataclass
class AtlasImage(HasUID):
    # Reference to the atlas that this image belongs to
    atlas: 'Atlas' = field(default_factory=lambda: Atlas())
    # Position of top left corner of image within the atlas
    pos: IntCoord = field(default_factory=IntCoord)
    # Optional name for the image to better identify it
    name: str = ""

@dataclass
class Atlas(HasUID):
    parent: Optional['AtlasParent'] = None
    source: Optional[Image.Image] = None
    # Dict of images based on uid
    images: dict[int, AtlasImage] = field(default_factory=dict)
    children: dict[int, 'Atlas'] = field(default_factory=dict)
    # Size of the atlas
    size: IntCoord = field(default_factory=IntCoord)
    # Name for the atlas
    name: str = ""

@dataclass
class AtlasParent:
    parent: Atlas = field(default_factory=Atlas)
    # Position of top left corner of image within the atlas
    pos: IntCoord = field(default_factory=IntCoord)

@dataclass
class AnimProject:
    # Dict of atlases based on uid
    atlases: dict[int, Atlas] = field(default_factory=dict)
    objects_by_uid: dict[int, HasUID] = field(default_factory=dict)

    _current_uid: int = 0
    def get_new_uid(self) -> int:
        self._current_uid += 1
        return self._current_uid

    def register_object(self, obj: U) -> U:
        new_id = obj._uid or self.get_new_uid()
        if new_id in self.objects_by_uid and self.objects_by_uid[new_id] != obj:
            raise ValueError(f"Object with id {new_id} already exist")
        self.objects_by_uid[new_id] = obj
        obj._uid = new_id
        return obj

    def add_atlas(self, atlas: Atlas) -> None:
        self.register_object(atlas)
        obj_id = atlas._uid
        if obj_id in self.atlases and self.atlases[obj_id] != atlas:
            raise ValueError(f"Atlas with id {obj_id} already exist")
        self.atlases[obj_id] = atlas
