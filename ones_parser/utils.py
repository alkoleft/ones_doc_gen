import os


def find_objects(source_code_directory):
    return [{
        'type': path_lvl1,
        'sub_objects': find_sub_objects(os.path.join(source_code_directory, path_lvl1))
    } for path_lvl1 in os.listdir(source_code_directory)
        if os.path.isdir(os.path.join(source_code_directory, path_lvl1))
    ]


def find_sub_objects(sub_directory):
    return [{
        'name': path_lvl2[0: -4],
        'file_name': os.path.join(sub_directory, path_lvl2)
    } for path_lvl2 in os.listdir(sub_directory)
        if os.path.isfile(os.path.join(sub_directory, path_lvl2)) and path_lvl2.endswith('.xml')
    ]


def find_modules(path):
    return [file for file in os.listdir(path) if file.endswith('.bsl')] \
        if os.path.exists(path) \
        else []


def create_if_not_exists(path):
    if not os.path.exists(path):
        create_if_not_exists(os.path.dirname(path))
        os.mkdir(path)
