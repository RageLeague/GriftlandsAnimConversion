from dataclasses import dataclass, field
BUILD_VERSION = 10
ANIM_VERSION = 7

def to_hex(int_val: int) -> str:
    return "0x{0:08X}".format(int_val)

@dataclass
class Coord:
    x: float = 0.0
    y: float = 0.0

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

@dataclass
class BBox:
    pos: Coord = field(default_factory=Coord)
    size: Coord = field(default_factory=Coord)

    def __str__(self) -> str:
        return f"[pos={self.pos}, size={self.size}]"

    def __repr__(self) -> str:
        return str(self)

@dataclass
class HashedString:
    hash_val: int = 0
    original: str = ""

    def __str__(self) -> str:
        return f"'{self.original}'[{to_hex(self.hash_val)}]"

    def __repr__(self) -> str:
        return str(self)

@dataclass
class BuildFrame:
    frame_num: int = 0
    duration: int = 0
    image_index: int = 0
    bbox: BBox = field(default_factory=BBox)
    uv0: Coord = field(default_factory=Coord)
    uv1: Coord = field(default_factory=Coord)

@dataclass
class BuildSymbol:
    symbol_hash: int = 0
    color_channel_hash: int = 0
    looping: bool = False
    frames: list[BuildFrame] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Symbol {to_hex(self.symbol_hash)} ({len(self.frames)} frames)"

    def __repr__(self) -> str:
        return str(self)

@dataclass
class BuildFile:
    version: int = BUILD_VERSION
    total_frames: int = 0
    build_name: str = ""
    materials: list[str] = field(default_factory=list)
    sdf_materials: list[str] = field(default_factory=list)
    symbols: list[BuildSymbol] = field(default_factory=list)
    hashed_strings: list[HashedString] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Build '{self.build_name}' ({len(self.symbols)} symbols)"

    def __repr__(self) -> str:
        return str(self)
