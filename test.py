from source.ganim_io import GriftAnimIO
with open(r'raw_files/anim.zip/build.bin', 'rb') as file:
    result = GriftAnimIO.read_build_file(file)
    print(result)
    with open(r'raw_files/anim.zip/build_copy.bin', 'wb') as file:
        GriftAnimIO.write_build_file(file, result)
