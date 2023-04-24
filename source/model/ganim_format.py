from dataclasses import dataclass, field
from PIL import Image
from typing import Optional, Protocol
BUILD_VERSION = 10
ANIM_VERSION = 7

def to_hex(int_val: int) -> str:
    return "0x{0:08X}".format(int_val)

@dataclass
class Coord:
    x: float = 0.0
    y: float = 0.0

@dataclass
class BBox:
    pos: Coord = field(default_factory=Coord)
    size: Coord = field(default_factory=Coord)

class HasHashStrings(Protocol):
    def get_hash_string(self, hash_val: int) -> str:
        ...

@dataclass
class HashRef:
    hash_val: int = 0
    table: Optional[HasHashStrings] = None
    def get_hash_string(self) -> str:
        if self.table is None:
            raise ValueError("Field 'table' is None")
        return self.table.get_hash_string(self.hash_val)
    def __str__(self) -> str:
        try:
            return self.get_hash_string()
        except Exception:
            return f"HashRef({to_hex(self.hash_val)})"
    def __repr__(self) -> str:
        return str(self)

@dataclass
class BuildFrame:
    frame_num: int = 0
    duration: int = 0
    # The index of the material that the image is chosen from (between 0 and len(materials) - 1)
    image_index: int = 0
    bbox: BBox = field(default_factory=BBox)
    # The top left corner of the image in the material
    # Ranges from (0.0, 0.0) (top left) to (1.0, 1.0) (bottom right)
    uv0: Coord = field(default_factory=Coord)
    # The bottom right corner of the image in the material
    uv1: Coord = field(default_factory=Coord)

@dataclass
class BuildSymbol:
    symbol_hash: HashRef = field(default_factory=HashRef)
    color_channel_hash: HashRef = field(default_factory=HashRef)
    looping: bool = False
    frames: list[BuildFrame] = field(default_factory=list)

@dataclass
class BuildMaterial:
    path: str = ""
    image: Optional[Image.Image] = None

@dataclass
class BuildFile:
    version: int = BUILD_VERSION
    total_frames: int = 0
    build_name: str = ""
    materials: list[BuildMaterial] = field(default_factory=list)
    sdf_materials: list[str] = field(default_factory=list)
    symbols: list[BuildSymbol] = field(default_factory=list)
    hashed_strings: dict[int, str] = field(default_factory=dict)
    def get_hash_string(self, hash_val: int) -> str:
        return self.hashed_strings[hash_val]

@dataclass
class AnimElement:
    symbol_hash: HashRef = field(default_factory=HashRef)
    frame: int = 0
    folder_hash: HashRef = field(default_factory=HashRef)

    # Color modifier of element. Multiplicative. Ranges from [0.0, 1.0]. Note the reverse order
    c_ap: float = 0.0
    c_bp: float = 0.0
    c_gp: float = 0.0
    c_rp: float = 0.0

    # Color modifier of element. Additive. Ranges from [0.0, 1.0]. Note the reverse order
    c_aa: float = 0.0
    c_ba: float = 0.0
    c_ga: float = 0.0
    c_ra: float = 0.0

    # Affine transformation matrix
    # https://helpx.adobe.com/flash/webgl-runtime-api-help/matrix.html
    mat_a: float = 0.0
    mat_b: float = 0.0
    mat_c: float = 0.0
    mat_d: float = 0.0
    tx: float = 0.0
    ty: float = 0.0

    # Index? The ordering for the element
    tz: float = 0.0

    def __str__(self) -> str:
        return f"AnimElement {self.symbol_hash} (frame {self.frame})"

    def __repr__(self) -> str:
        return str(self)

@dataclass
class AnimFrame:
    pos: Coord = field(default_factory=Coord)
    size: Coord = field(default_factory=Coord)
    elements: list[AnimElement] = field(default_factory=list)

@dataclass
class AnimData:
    anim_name: str = ""
    root_symbol: str = ""
    frame_rate: float = 0.0
    looping: bool = False
    frames: list[AnimFrame] = field(default_factory=list)

@dataclass
class AnimFile:
    version: int = ANIM_VERSION
    num_element_refs: int = 0
    num_frames: int = 0
    anims: list[AnimData] = field(default_factory=list)
    hashed_strings: dict[int, str] = field(default_factory=dict)
    def get_hash_string(self, hash_val: int) -> str:
        return self.hashed_strings[hash_val]

@dataclass
class Animation:
    build: Optional[BuildFile] = None
    anim: Optional[AnimFile] = None
