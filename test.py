from source.model.ganim_io import GriftAnimIO
import struct
from source.model.image_format import *
from source.model.util import overlay_atlas

# anim = GriftAnimIO.read_animation("raw_files/test_slide.zip")
head = GriftAnimIO.read_animation("raw_files/test.zip")
# build = GriftAnimIO.read_animation("raw_files/test_build.zip")
pass
# overlay_atlas(animation)
# if animation.build.materials[0].image:
#     write_png("raw_files/anim_copy.zip/processed.png", animation.build.materials[0].image)
# GriftAnimIO.write_animation("raw_files/anim_copy.zip", animation)
# print(animation)

# image = read_png("raw_files/test.zip/atlas0.png")
# print(image)
# write_ktex("raw_files/test.zip/atlas0.tex", image)

# write_png("raw_files/anim.zip/atlas0.png", read_ktex("raw_files/anim.zip/atlas0.tex"))
# write_png("raw_files/anim.zip/atlas0_copy.png", read_ktex("raw_files/anim.zip/atlas0_copy.tex"))

# packed = struct.pack(">ffff", 1.0, 2.0, 4.0, 8.0)
# for i in range(4):
#     print(struct.unpack(">f", packed[i * 4 : (i + 1) * 4]))
# with open(r'raw_files/anim.zip/build.bin', 'rb') as file:
#     result = GriftAnimIO.read_build_file(file)
#     print(result)
#     with open(r'raw_files/anim.zip/build_copy.bin', 'wb') as file:
#         GriftAnimIO.write_build_file(file, result)

# with open(r'raw_files/anim.zip/anim.bin', 'rb') as file:
#     result = GriftAnimIO.read_anim_file(file)
#     print(result)
#     with open(r'raw_files/anim.zip/anim_copy.bin', 'wb') as file:
#         GriftAnimIO.write_anim_file(file, result)
