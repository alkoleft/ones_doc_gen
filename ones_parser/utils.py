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


def get_obj_directory(source_code_directory, obj):
    return os.path.join(source_code_directory, obj.collectionName, obj.name)


def get_obj_file(source_code_directory, obj):
    return os.path.join(source_code_directory, obj.collectionName, obj.name + '.xml')


def find_modules(path):

    return [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.bsl')] \
        if os.path.exists(path) \
        else []
