from typing import IO
from source.ganim_format import BuildFile, AnimFile

class AnimFileIO:
    @staticmethod
    def read_build_file(file: IO) -> BuildFile:
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def write_build_file(file: IO, build: BuildFile) -> None:
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def read_anim_file(file: IO) -> AnimFile:
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def write_anim_file(file: IO, anim: AnimFile) -> None:
        raise NotImplementedError("Method not implemented")

class WrongFormatException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
