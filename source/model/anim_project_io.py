from PIL import Image
import json, os

from source.model.anim_project import AnimProject
from source.model.image_format import write_image

def save_project(file: str, project: AnimProject) -> None:
    proj_json, asset_dict = project.save_json()
    with open(file, "w") as proj_file:
        json.dump(proj_json, proj_file)
    asset_path = os.path.basename(file) + "_assets"
    if not os.path.exists(asset_path):
        os.makedirs(asset_path)
    for path in asset_dict:
        obj = asset_dict[path]
        if isinstance(obj, Image.Image):
            write_image(os.path.join(asset_path, path), obj)

def load_project(file: str) -> AnimProject:
    asset_path = os.path.basename(file) + "_assets"
    with open(file, "w") as proj_file:
        obj = json.load(proj_file)
        project = AnimProject()

        project.load_json(obj, asset_path)

        return project
