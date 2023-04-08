from source.model.ganim_format import Animation

class AnimFileIO:
    @staticmethod
    def read_animation(animation_folder: str) -> Animation:
        raise NotImplementedError("Function not implemented")

    @staticmethod
    def write_animation(animation_folder: str, animation: Animation) -> None:
        raise NotImplementedError("Function not implemented")

class WrongFormatException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
