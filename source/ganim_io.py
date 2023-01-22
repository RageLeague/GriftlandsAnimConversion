from typing import IO, BinaryIO, Any
from source.ganim_format import *
from source.file_io import AnimFileIO
from struct import pack, unpack, calcsize

ENCODING = "utf-8"
BUILD_STRING = "BILD"

class GriftAnimIO(AnimFileIO):
    ### Some general methods for I/O
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

        return output.decode(ENCODING)

    @staticmethod
    def read_hashed_string(file: BinaryIO) -> HashedString:
        result = HashedString()
        result.hash_val = GriftAnimIO.read_int(file)
        result.original = GriftAnimIO.read_str(file)
        return result

    @staticmethod
    def write(file: BinaryIO, fmt: str, obj: Any) -> None:
        bin = pack(fmt, obj)
        file.write(bin)

    @staticmethod
    def write_int(file: BinaryIO, val: int) -> None:
        GriftAnimIO.write(file, "I", val)

    @staticmethod
    def write_bool(file: BinaryIO, val: bool) -> None:
        GriftAnimIO.write_int(file, 1 if val else 0)

    @staticmethod
    def write_float(file: BinaryIO, val: float) -> None:
        GriftAnimIO.write(file, "f", val)

    @staticmethod
    def write_string(file: BinaryIO, val: str, include_size = True) -> None:
        if include_size:
            GriftAnimIO.write_int(file, len(val))
        for b in val:
            GriftAnimIO.write(file, "s", bytes(b, ENCODING))

    @staticmethod
    def write_hashed_string(file: BinaryIO, val: HashedString) -> None:
        GriftAnimIO.write_int(file, val.hash_val)
        GriftAnimIO.write_string(file, val.original)

    ### Methods for reading the build file

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
    def read_build_file(file: BinaryIO) -> BuildFile:
        header = file.read(len(BUILD_STRING)).decode("utf-8")
        if header != BUILD_STRING:
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

    ### Methods for writing the build file

    @staticmethod
    def write_build_frame(file: BinaryIO, frame: BuildFrame) -> None:
        GriftAnimIO.write_int(file, frame.frame_num)
        GriftAnimIO.write_int(file, frame.duration)
        GriftAnimIO.write_int(file, frame.image_index)
        GriftAnimIO.write_float(file, frame.bbox.pos.x)
        GriftAnimIO.write_float(file, frame.bbox.pos.y)
        GriftAnimIO.write_float(file, frame.bbox.size.x)
        GriftAnimIO.write_float(file, frame.bbox.size.y)
        GriftAnimIO.write_float(file, frame.uv0.x)
        GriftAnimIO.write_float(file, frame.uv0.y)
        GriftAnimIO.write_float(file, frame.uv1.x)
        GriftAnimIO.write_float(file, frame.uv1.y)

    @staticmethod
    def write_build_symbol(file: BinaryIO, symbol: BuildSymbol) -> None:
        GriftAnimIO.write_int(file, symbol.symbol_hash)
        GriftAnimIO.write_int(file, symbol.color_channel_hash)
        GriftAnimIO.write_bool(file, symbol.looping)
        GriftAnimIO.write_int(file, len(symbol.frames))
        for frame in symbol.frames:
            GriftAnimIO.write_build_frame(file, frame)

    @staticmethod
    def write_build_file(file: BinaryIO, build: BuildFile) -> None:
        GriftAnimIO.write_string(file, BUILD_STRING, False)
        GriftAnimIO.write_int(file, build.version)
        GriftAnimIO.write_int(file, len(build.symbols))
        GriftAnimIO.write_int(file, build.total_frames)
        GriftAnimIO.write_string(file, build.build_name)
        GriftAnimIO.write_int(file, len(build.materials))
        for material in build.materials:
            GriftAnimIO.write_string(file, material)
        GriftAnimIO.write_int(file, len(build.sdf_materials))
        for material in build.sdf_materials:
            GriftAnimIO.write_string(file, material)
        for symbol in build.symbols:
            GriftAnimIO.write_build_symbol(file, symbol)
        GriftAnimIO.write_int(file, len(build.hashed_strings))
        for string in build.hashed_strings:
            GriftAnimIO.write_hashed_string(file, string)
