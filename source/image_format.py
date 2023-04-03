from PIL import Image
import io, os
from struct import pack, unpack
from typing import Optional

KTEX_VERSION = 2

def read_ktex(filename: str) -> Image.Image:
    with open(filename, "rb") as infile:
        magic=infile.read(4)
        disc=infile.read(5)

        if magic==b"KTEX":
            data=infile.read()
        elif b"DDS" in magic:
            infile.seek(0)
            data=infile.read()
        else:
            raise ValueError()

    image=Image.open(io.BytesIO(data))
    return image

def write_ktex(filename: str, image: Image.Image) -> None:
    with open(filename, "wb") as outfile:
        # Write magic word
        outfile.write(b"KTEX")
        # Write version
        outfile.write(pack("<B", KTEX_VERSION))
        width, height = image.size
        outfile.write(pack("<H", width))
        outfile.write(pack("<H", height))
        # Write actual file content
        image.save(outfile, "DDS")

def read_dds(filename: str) -> Image.Image:
    return Image.open(filename, formats=["DDS"])

def write_dds(filename: str, image: Image.Image) -> None:
    image.save(filename, "DDS")

def read_png(filename: str) -> Image.Image:
    return Image.open(filename, formats=["PNG"])

def write_png(filename: str, image: Image.Image) -> None:
    image.save(filename, "PNG")

def read_image(filename: str, extension: Optional[str] = None) -> Image.Image:
    if extension is None:
        _, extension = os.path.splitext(filename)
    if extension.lower() == ".tex":
        return read_ktex(filename)
    elif extension.lower() == ".dds":
        return read_dds(filename)
    elif extension.lower() == ".png":
        return read_png(filename)
    raise ValueError()

def write_image(filename: str, image: Image.Image, extension: Optional[str] = None) -> None:
    if extension is None:
        _, extension = os.path.splitext(filename)
    if extension.lower() == ".tex":
        write_ktex(filename, image)
        return
    elif extension.lower() == ".dds":
        write_dds(filename, image)
        return
    elif extension.lower() == ".png":
        write_png(filename, image)
        return
    raise ValueError()
