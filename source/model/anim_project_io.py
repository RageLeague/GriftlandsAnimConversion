from PIL import Image
import json, os

from source.model.anim_project import AnimProject
from source.model.image_format import write_image

def save_project(folder: str, project: AnimProject) -> None:
    proj_json, asset_dict = project.save_json()
    with open(os.path.join(folder, "project.json"), "w") as proj_file:
        json.dump(proj_json, proj_file)
    for path in asset_dict:
        obj = asset_dict[path]
        if isinstance(obj, Image.Image):
            write_image(os.path.join(folder, "assets", path), obj)
