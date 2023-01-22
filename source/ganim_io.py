from typing import IO, BinaryIO
from source.ganim_format import *
from source.file_io import AnimFileIO
from struct import unpack, calcsize

class GriftAnimIO(AnimFileIO):
    @staticmethod
    def read(file: BinaryIO, fmt: str):
        size = calcsize(fmt)
        val = file.read(size)

        if size != len(val):
            raise EOFError("EOF reached")

        return unpack(fmt, val)[0]

    @staticmethod
    def read_int(file: BinaryIO) -> int:
        return GriftAnimIO.read(file, "I")

    @staticmethod
    def read_float(file: BinaryIO) -> float:
        return GriftAnimIO.read(file, "f")

    # Read string from a binary file
    # If no size is provided, read the size from file as the size
    @staticmethod
    def read_str(file: BinaryIO, size: int | None = None) -> str:
        if size is None:
            size = GriftAnimIO.read_int(file)
        assert(size is not None)
        output = b""

        for _ in range(size):
            output += GriftAnimIO.read(file, "s")

        return output.decode("utf-8")

    @staticmethod
    def read_build_frame(file: BinaryIO) -> BuildFrame:
        result = BuildFrame()
        result.frame_num = GriftAnimIO.read_int(file)
        result.duration = GriftAnimIO.read_int(file)
        result.image_index = GriftAnimIO.read_int(file)
        result.bbox.pos.x = GriftAnimIO.read_float(file)
        result.bbox.pos.y = GriftAnimIO.read_float(file)
        result.bbox.size.x = GriftAnimIO.read_float(file)
        result.bbox.size.y = GriftAnimIO.read_float(file)
        result.uv0.x = GriftAnimIO.read_float(file)
        result.uv0.y = GriftAnimIO.read_float(file)
        result.uv1.x = GriftAnimIO.read_float(file)
        result.uv1.y = GriftAnimIO.read_float(file)
        return result

    @staticmethod
    def read_build_symbol(file: BinaryIO) -> BuildSymbol:
        result = BuildSymbol()
        result.symbol_hash = GriftAnimIO.read_int(file)
        result.color_channel_hash = GriftAnimIO.read_int(file)
        result.looping = GriftAnimIO.read_int(file) != 0
        num_frames = GriftAnimIO.read_int(file)
        for _ in range(num_frames):
            result.frames.append(GriftAnimIO.read_build_frame(file))
        return result

    @staticmethod
    def read_hashed_string(file: BinaryIO) -> HashedString:
        result = HashedString()
        result.hash_val = GriftAnimIO.read_int(file)
        result.original = GriftAnimIO.read_str(file)
        return result

    @staticmethod
    def read_build_file(file: BinaryIO) -> BuildFile:
        header = file.read(4).decode("utf-8")
        if header != 'BILD':
            raise Exception("Header must be BILD")
        result = BuildFile()
        result.version = GriftAnimIO.read_int(file)
        total_symbols = GriftAnimIO.read_int(file)
        result.total_frames = GriftAnimIO.read_int(file)
        result.build_name = GriftAnimIO.read_str(file)
        num_materials = GriftAnimIO.read_int(file)
        for _ in range(num_materials):
            result.materials.append(GriftAnimIO.read_str(file))
        num_sdf_materials = GriftAnimIO.read_int(file)
        for _ in range(num_sdf_materials):
            result.sdf_materials.append(GriftAnimIO.read_str(file))
        for _ in range(total_symbols):
            result.symbols.append(GriftAnimIO.read_build_symbol(file))
        num_hashed_strings = GriftAnimIO.read_int(file)
        for _ in range(num_hashed_strings):
            result.hashed_strings.append(GriftAnimIO.read_hashed_string(file))
        return result
