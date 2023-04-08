from source.ganim_format import *
from PIL import Image, ImageDraw

colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]

def overlay_atlas(anim: Animation) -> None:
    # Set of tuples: (index, x1, y1, x2, y2)
    seen_box: set[tuple[int, int, int, int, int]] = set()
    if not anim.build:
        return
    for symbol in anim.build.symbols:
        for frame in symbol.frames:
            material = anim.build.materials[frame.image_index]
            if material.image is not None:
                mat_w, mat_h = material.image.size
                x1, y1 = round(mat_w * frame.uv0.x), round(mat_h * frame.uv0.y)
                x2, y2 = round(mat_w * frame.uv1.x), round(mat_h * frame.uv1.y)
                id = (frame.image_index, x1, y1, x2, y2)
                if id not in seen_box:
                    mask = Image.new("L", (x2 - x1, y2 - y1), 50)
                    material.image.paste(colors[len(seen_box) % len(colors)], (x1, y1, x2, y2), mask)
                    seen_box.add(id)
