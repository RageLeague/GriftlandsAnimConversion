BUILD_VERSION = 10
ANIM_VERSION = 7

def to_hex(int_val: int) -> str:
    return "0x{0:08X}".format(int_val)

class Coord:
    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __repr__(self) -> str:
        return str(self)

class BBox:
    def __init__(self, pos: Coord | None = None, size: Coord | None = None) -> None:
        self.pos = pos or Coord()
        self.size = size or Coord()

    def __str__(self) -> str:
        return f"[pos={self.pos}, size={self.size}]"

    def __repr__(self) -> str:
        return str(self)

class HashedString:
    def __init__(self, hash_val = 0, original = "") -> None:
        self.hash_val = hash_val
        self.original = original

    def __str__(self) -> str:
        return f"'{self.original}'[{to_hex(self.hash_val)}]"

    def __repr__(self) -> str:
        return str(self)

class BuildFrame:
    def __init__(
        self,
        frame_num = 0,
        duration = 0,
        image_index = 0,
        bbox: BBox | None = None,
        uv0: Coord | None = None,
        uv1: Coord | None = None
    ) -> None:
        self.frame_num = frame_num
        self.duration = duration
        self.image_index = image_index
        self.bbox = bbox or BBox()
        self.uv0 = uv0 or Coord()
        self.uv1 = uv1 or Coord()


class BuildSymbol:
    def __init__(self, symbol_hash = 0, color_channel_hash = 0, looping = False, frames: list[BuildFrame] | None = None) -> None:
        self.symbol_hash = symbol_hash
        self.color_channel_hash = color_channel_hash
        self.looping = looping
        self.frames = frames or []

    def __str__(self) -> str:
        return f"Symbol {to_hex(self.symbol_hash)} ({len(self.frames)} frames)"

    def __repr__(self) -> str:
        return str(self)

class BuildFile:
    def __init__(self, version = BUILD_VERSION, total_frames = 0, build_name = "", materials: list[str] | None = None, sdf_materials: list[str] | None = None, symbols: list[BuildSymbol] | None = None, hashed_strings: list[HashedString] | None = None) -> None:
        self.version = version
        self.total_frames = total_frames
        self.build_name = build_name
        self.materials = materials or []
        self.sdf_materials = sdf_materials or []
        self.symbols = symbols or []
        self.hashed_strings = hashed_strings or []

    def __str__(self) -> str:
        return f"Build '{self.build_name}' ({len(self.symbols)} symbols)"

    def __repr__(self) -> str:
        return str(self)
