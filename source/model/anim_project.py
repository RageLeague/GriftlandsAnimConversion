from dataclasses import dataclass, field
from PIL import Image
from typing import Optional, TypeVar, Generic, Any

T = TypeVar("T")

@dataclass
class IntCoord:
    x: int = 0
    y: int = 0

@dataclass
class HasUID:
    _uid: int = 0

U = TypeVar("U", bound=HasUID)

@dataclass
class UIDRef(Generic[T]):
    obj_type: type[T] = field()
    project: 'AnimProject' | None = None
    uid: int = 0

    def get(self) -> T:
        if self.project is None:
            raise ValueError(f"Field 'project' is None")
        if self.uid not in self.project.objects_by_uid:
            raise ValueError(f"Object with uid {self.uid} does not exist")
        obj: Any = self.project.objects_by_uid[self.uid]
        if not isinstance(obj, self.obj_type):
            raise ValueError(f"Object with uid {self.uid} is not of type {self.obj_type}")
        return obj

@dataclass
class AtlasImage(HasUID):
    # Reference to the atlas that this image belongs to
    atlas: UIDRef['Atlas'] = field(default_factory=lambda: UIDRef(Atlas))
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
        new_id = self.get_new_uid()
        self.objects_by_uid[new_id] = obj
        obj._uid = new_id
        return obj
