from typing import IO, BinaryIO
from source.ganim_format import *
from struct import unpack, calcsize



class AnimFileFormat:
    @staticmethod
    def read_build_file(file: IO) -> BuildFile:
        raise NotImplementedError("Method not implemented")

class GriftAnimFormat(AnimFileFormat):
    @staticmethod
    def read(file: BinaryIO, fmt: str):
        size = calcsize(fmt)
        val = file.read(size)

        if size != len(val):
            raise EOFError("EOF reached")

        return unpack(fmt, val)[0]

    @staticmethod
    def read_int(file: BinaryIO) -> int:
        return GriftAnimFormat.read(file, "I")

    @staticmethod
    def read_float(file: BinaryIO) -> float:
        return GriftAnimFormat.read(file, "f")

    # Read string from a binary file
    # If no size is provided, read the size from file as the size
    @staticmethod
    def read_str(file: BinaryIO, size: int | None = None) -> str:
        if size is None:
            size = GriftAnimFormat.read_int(file)
        assert(size is not None)
        output = b""

        for _ in range(size):
            output += GriftAnimFormat.read(file, "s")

        return output.decode("utf-8")

    @staticmethod
    def read_build_frame(file: BinaryIO) -> BuildFrame:
        result = BuildFrame()
        result.frame_num = GriftAnimFormat.read_int(file)
        result.duration = GriftAnimFormat.read_int(file)
        result.image_index = GriftAnimFormat.read_int(file)
        result.bbox.pos.x = GriftAnimFormat.read_float(file)
        result.bbox.pos.y = GriftAnimFormat.read_float(file)
        result.bbox.size.x = GriftAnimFormat.read_float(file)
        result.bbox.size.y = GriftAnimFormat.read_float(file)
        result.uv0.x = GriftAnimFormat.read_float(file)
        result.uv0.y = GriftAnimFormat.read_float(file)
        result.uv1.x = GriftAnimFormat.read_float(file)
        result.uv1.y = GriftAnimFormat.read_float(file)
        return result

    @staticmethod
    def read_build_symbol(file: BinaryIO) -> BuildSymbol:
        result = BuildSymbol()
        result.symbol_hash = GriftAnimFormat.read_int(file)
        result.color_channel_hash = GriftAnimFormat.read_int(file)
        result.looping = GriftAnimFormat.read_int(file) != 0
        num_frames = GriftAnimFormat.read_int(file)
        for _ in range(num_frames):
            result.frames.append(GriftAnimFormat.read_build_frame(file))
        return result

    @staticmethod
    def read_hashed_string(file: BinaryIO) -> HashedString:
        result = HashedString()
        result.hash_val = GriftAnimFormat.read_int(file)
        result.original = GriftAnimFormat.read_str(file)
        return result

    @staticmethod
    def read_build_file(file: BinaryIO) -> BuildFile:
        header = file.read(4).decode("utf-8")
        if header != 'BILD':
            raise Exception("Header must be BILD")
        result = BuildFile()
        result.version = GriftAnimFormat.read_int(file)
        total_symbols = GriftAnimFormat.read_int(file)
        result.total_frames = GriftAnimFormat.read_int(file)
        result.build_name = GriftAnimFormat.read_str(file)
        num_materials = GriftAnimFormat.read_int(file)
        for _ in range(num_materials):
            result.materials.append(GriftAnimFormat.read_str(file))
        num_sdf_materials = GriftAnimFormat.read_int(file)
        for _ in range(num_sdf_materials):
            result.sdf_materials.append(GriftAnimFormat.read_str(file))
        for _ in range(total_symbols):
            result.symbols.append(GriftAnimFormat.read_build_symbol(file))
        num_hashed_strings = GriftAnimFormat.read_int(file)
        for _ in range(num_hashed_strings):
            result.hashed_strings.append(GriftAnimFormat.read_hashed_string(file))
        return result

