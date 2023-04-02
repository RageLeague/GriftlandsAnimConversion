from PIL import Image
import io
from struct import pack, unpack

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
            raise ValueError("Invalid .tex file")

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
