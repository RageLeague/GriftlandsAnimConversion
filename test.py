from source.file_format import GriftAnimFormat
with open(r'raw_files\anim.zip\build.bin', 'rb') as file:
    result = GriftAnimFormat.read_build_file(file)
    print(result)
