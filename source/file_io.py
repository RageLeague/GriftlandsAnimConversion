from typing import IO
from source.ganim_format import BuildFile

class AnimFileIO:
    @staticmethod
    def read_build_file(file: IO) -> BuildFile:
        raise NotImplementedError("Method not implemented")

    @staticmethod
    def write_build_file(file: IO, build: BuildFile) -> None:
        raise NotImplementedError("Method not implemented")
