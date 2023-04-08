from typing import BinaryIO, Any
from source.ganim_format import *
from source.file_io import AnimFileIO, WrongFormatException
from source.image_format import read_image, write_image
from struct import pack, unpack, calcsize
import os

ENCODING = "utf-8"
BUILD_STRING = "BILD"
ANIM_STRING = "ANIM"

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
        return GriftAnimIO.read(file, "<I")

    @staticmethod
    def read_bool(file: BinaryIO) -> bool:
        return bool(GriftAnimIO.read_int(file))

    @staticmethod
    def read_float(file: BinaryIO) -> float:
        return GriftAnimIO.read(file, "<f")

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
    def write(file: BinaryIO, fmt: str, obj: Any) -> None:
        bin = pack(fmt, obj)
        file.write(bin)

    @staticmethod
    def write_int(file: BinaryIO, val: int) -> None:
        GriftAnimIO.write(file, "<I", val)

    @staticmethod
    def write_bool(file: BinaryIO, val: bool) -> None:
        GriftAnimIO.write_int(file, 1 if val else 0)

    @staticmethod
    def write_float(file: BinaryIO, val: float) -> None:
        GriftAnimIO.write(file, "<f", val)

    @staticmethod
    def write_str(file: BinaryIO, val: str, include_size = True) -> None:
        if include_size:
            GriftAnimIO.write_int(file, len(val))
        for b in val:
            GriftAnimIO.write(file, "s", bytes(b, ENCODING))

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
    def read_build_symbol(file: BinaryIO, build_file: BuildFile) -> BuildSymbol:
        result = BuildSymbol()
        result.symbol_hash = HashRef(GriftAnimIO.read_int(file), build_file)
        result.color_channel_hash = HashRef(GriftAnimIO.read_int(file), build_file)
        result.looping = GriftAnimIO.read_bool(file)
        num_frames = GriftAnimIO.read_int(file)
        for _ in range(num_frames):
            result.frames.append(GriftAnimIO.read_build_frame(file))
        return result

    @staticmethod
    def read_build_file(file: BinaryIO, folder_path: str) -> BuildFile:
        header = file.read(len(BUILD_STRING)).decode("utf-8")
        if header != BUILD_STRING:
            raise WrongFormatException("Header must be {BUILD_STRING}")
        result = BuildFile()
        result.version = GriftAnimIO.read_int(file)
        if result.version == BUILD_VERSION:
            total_symbols = GriftAnimIO.read_int(file)
            result.total_frames = GriftAnimIO.read_int(file)
            result.build_name = GriftAnimIO.read_str(file)
            num_materials = GriftAnimIO.read_int(file)
            for _ in range(num_materials):
                material_name = GriftAnimIO.read_str(file)
                image = read_image(os.path.join(folder_path, material_name))
                result.materials.append(BuildMaterial(material_name, image))
            num_sdf_materials = GriftAnimIO.read_int(file)
            for _ in range(num_sdf_materials):
                result.sdf_materials.append(GriftAnimIO.read_str(file))
            for _ in range(total_symbols):
                result.symbols.append(GriftAnimIO.read_build_symbol(file, result))
            num_hashed_strings = GriftAnimIO.read_int(file)
            for _ in range(num_hashed_strings):
                hash_val = GriftAnimIO.read_int(file)
                hash_str = GriftAnimIO.read_str(file)
                result.hashed_strings[hash_val] = hash_str
            if file.read(1):
                raise WrongFormatException("End of file not reached")
            return result
        raise WrongFormatException("Invalid version")

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
        GriftAnimIO.write_int(file, symbol.symbol_hash.hash_val)
        GriftAnimIO.write_int(file, symbol.color_channel_hash.hash_val)
        GriftAnimIO.write_bool(file, symbol.looping)
        GriftAnimIO.write_int(file, len(symbol.frames))
        for frame in symbol.frames:
            GriftAnimIO.write_build_frame(file, frame)

    @staticmethod
    def write_build_file(file: BinaryIO, folder_path: str, build: BuildFile) -> None:
        GriftAnimIO.write_str(file, BUILD_STRING, False)
        GriftAnimIO.write_int(file, BUILD_VERSION)
        GriftAnimIO.write_int(file, len(build.symbols))
        GriftAnimIO.write_int(file, build.total_frames)
        GriftAnimIO.write_str(file, build.build_name)
        GriftAnimIO.write_int(file, len(build.materials))
        for material in build.materials:
            GriftAnimIO.write_str(file, material.path)
            if material.image:
                write_image(os.path.join(folder_path, material.path), material.image)
        GriftAnimIO.write_int(file, len(build.sdf_materials))
        for material in build.sdf_materials:
            GriftAnimIO.write_str(file, material)
        for symbol in build.symbols:
            GriftAnimIO.write_build_symbol(file, symbol)
        GriftAnimIO.write_int(file, len(build.hashed_strings))
        for hash_val in build.hashed_strings:
            GriftAnimIO.write_int(file, hash_val)
            GriftAnimIO.write_str(file, build.hashed_strings[hash_val])

    @staticmethod
    def read_anim_element(file: BinaryIO, anim_file: AnimFile) -> AnimElement:
        result = AnimElement()
        result.symbol_hash = HashRef(GriftAnimIO.read_int(file), anim_file)
        result.frame = GriftAnimIO.read_int(file)
        result.folder_hash = HashRef(GriftAnimIO.read_int(file), anim_file)

        result.c_ap = GriftAnimIO.read_float(file)
        result.c_bp = GriftAnimIO.read_float(file)
        result.c_gp = GriftAnimIO.read_float(file)
        result.c_rp = GriftAnimIO.read_float(file)

        result.c_aa = GriftAnimIO.read_float(file)
        result.c_ba = GriftAnimIO.read_float(file)
        result.c_ga = GriftAnimIO.read_float(file)
        result.c_ra = GriftAnimIO.read_float(file)

        result.mat_a = GriftAnimIO.read_float(file)
        result.mat_b = GriftAnimIO.read_float(file)
        result.mat_c = GriftAnimIO.read_float(file)
        result.mat_d = GriftAnimIO.read_float(file)
        result.tx = GriftAnimIO.read_float(file)
        result.ty = GriftAnimIO.read_float(file)
        result.tz = GriftAnimIO.read_float(file)

        return result

    @staticmethod
    def read_anim_frame(file: BinaryIO, anim_file: AnimFile) -> AnimFrame:
        result = AnimFrame()
        result.pos.x = GriftAnimIO.read_float(file)
        result.pos.y = GriftAnimIO.read_float(file)
        result.size.x = GriftAnimIO.read_float(file)
        result.size.y = GriftAnimIO.read_float(file)
        num_e = GriftAnimIO.read_int(file)
        for _ in range(num_e):
            result.elements.append(GriftAnimIO.read_anim_element(file, anim_file))
        return result

    @staticmethod
    def read_anim_data(file: BinaryIO, anim_file: AnimFile) -> AnimData:
        result = AnimData()
        result.anim_name = GriftAnimIO.read_str(file)
        result.root_symbol = GriftAnimIO.read_str(file)
        result.frame_rate = GriftAnimIO.read_float(file)
        result.looping = GriftAnimIO.read_bool(file)
        num_f = GriftAnimIO.read_int(file)
        for _ in range(num_f):
            result.frames.append(GriftAnimIO.read_anim_frame(file, anim_file))
        return result

    @staticmethod
    def read_anim_file(file: BinaryIO) -> AnimFile:
        header = file.read(len(ANIM_STRING)).decode("utf-8")
        if header != ANIM_STRING:
            raise WrongFormatException("Header must be {ANIM_STRING}")
        result = AnimFile()
        result.version = GriftAnimIO.read_int(file)
        if result.version == ANIM_VERSION:
            result.num_element_refs = GriftAnimIO.read_int(file)
            result.num_frames = GriftAnimIO.read_int(file)
            num_anims = GriftAnimIO.read_int(file)
            for _ in range(num_anims):
                result.anims.append(GriftAnimIO.read_anim_data(file, result))
            num_strings = GriftAnimIO.read_int(file)
            for _ in range(num_strings):
                hash_val = GriftAnimIO.read_int(file)
                hash_str = GriftAnimIO.read_str(file)
                result.hashed_strings[hash_val] = hash_str
            if file.read(1):
                raise WrongFormatException("End of file not reached")
            return result
        raise WrongFormatException("Invalid version")

    @staticmethod
    def write_anim_element(file: BinaryIO, element: AnimElement) -> None:
        GriftAnimIO.write_int(file, element.symbol_hash.hash_val)
        GriftAnimIO.write_int(file, element.frame)
        GriftAnimIO.write_int(file, element.folder_hash.hash_val)

        GriftAnimIO.write_float(file, element.c_ap)
        GriftAnimIO.write_float(file, element.c_bp)
        GriftAnimIO.write_float(file, element.c_gp)
        GriftAnimIO.write_float(file, element.c_rp)

        GriftAnimIO.write_float(file, element.c_aa)
        GriftAnimIO.write_float(file, element.c_ba)
        GriftAnimIO.write_float(file, element.c_ga)
        GriftAnimIO.write_float(file, element.c_ra)

        GriftAnimIO.write_float(file, element.mat_a)
        GriftAnimIO.write_float(file, element.mat_b)
        GriftAnimIO.write_float(file, element.mat_c)
        GriftAnimIO.write_float(file, element.mat_d)
        GriftAnimIO.write_float(file, element.tx)
        GriftAnimIO.write_float(file, element.ty)
        GriftAnimIO.write_float(file, element.tz)

    @staticmethod
    def write_anim_frame(file: BinaryIO, frame: AnimFrame) -> None:
        GriftAnimIO.write_float(file, frame.pos.x)
        GriftAnimIO.write_float(file, frame.pos.y)
        GriftAnimIO.write_float(file, frame.size.x)
        GriftAnimIO.write_float(file, frame.size.y)
        GriftAnimIO.write_int(file, len(frame.elements))
        for element in frame.elements:
            GriftAnimIO.write_anim_element(file, element)

    @staticmethod
    def write_anim_data(file: BinaryIO, data: AnimData) -> None:
        GriftAnimIO.write_str(file, data.anim_name)
        GriftAnimIO.write_str(file, data.root_symbol)
        GriftAnimIO.write_float(file, data.frame_rate)
        GriftAnimIO.write_bool(file, data.looping)
        GriftAnimIO.write_int(file, len(data.frames))
        for frame in data.frames:
            GriftAnimIO.write_anim_frame(file, frame)

    @staticmethod
    def write_anim_file(file: BinaryIO, anim: AnimFile) -> None:
        GriftAnimIO.write_str(file, ANIM_STRING, False)
        GriftAnimIO.write_int(file, ANIM_VERSION)
        GriftAnimIO.write_int(file, anim.num_element_refs)
        GriftAnimIO.write_int(file, anim.num_frames)
        GriftAnimIO.write_int(file, len(anim.anims))
        for one_anim in anim.anims:
            GriftAnimIO.write_anim_data(file, one_anim)
        GriftAnimIO.write_int(file, len(anim.hashed_strings))
        for hash_val in anim.hashed_strings:
            GriftAnimIO.write_int(file, hash_val)
            GriftAnimIO.write_str(file, anim.hashed_strings[hash_val])

    @staticmethod
    def read_animation(animation_folder: str) -> Animation:
        with open(os.path.join(animation_folder, "build.bin"), "rb") as build_file, open(os.path.join(animation_folder, "anim.bin"), "rb") as anim_file:
            build = GriftAnimIO.read_build_file(build_file, animation_folder)
            anim = GriftAnimIO.read_anim_file(anim_file)
            return Animation(build, anim)

    @staticmethod
    def write_animation(animation_folder: str, animation: Animation) -> None:
        if not os.path.exists(animation_folder):
            os.makedirs(animation_folder)

        with open(os.path.join(animation_folder, "build.bin"), "wb") as build_file, open(os.path.join(animation_folder, "anim.bin"), "wb") as anim_file:
            GriftAnimIO.write_build_file(build_file, animation_folder, animation.build)
            GriftAnimIO.write_anim_file(anim_file, animation.anim)
