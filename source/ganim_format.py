BUILD_VERSION = 10
ANIM_VERSION = 10

class Coord:
    def __init__(self, x = 0.0, y = 0.0) -> None:
        self.x = x
        self.y = y

class BBox:
    def __init__(self, pos: Coord = None, size: Coord = None) -> None:
        self.pos = pos or Coord()
        self.size = size or Coord()

class HashedString:
    def __init__(self, hash_val = 0, original = "") -> None:
        self.hash_val = hash_val
        self.original = original

class BuildFrame:
    def __init__(
        self,
        frame_num = 0,
        duration = 0,
        image_index = 0,
        bbox: BBox = None,
        uv0: Coord = None,
        uv1: Coord = None
    ) -> None:
        self.frame_num = frame_num
        self.duration = duration
        self.image_index = image_index
        self.bbox = bbox or BBox()
        self.uv0 = uv0 or Coord()
        self.uv1 = uv1 or Coord()


class BuildData:
    def __init__(self) -> None:
        pass
