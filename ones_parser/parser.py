import os
from . import parse_object_info
from .parsed_data.Configuration import Configuration, MetadataCollection
from .parsed_data.BaseMetadataObject import fabric
from . import utils
from . import module_parser

MODULES = 1
OBJECTS = 2


class Parser:

    def __init__(self, source_code_directory):
        self.source_code_directory = source_code_directory
        self.configuration = None

    def read_structure(self):
        files = dict()
        configuration = Configuration()

        for item in utils.find_objects(self.source_code_directory):
            collection = MetadataCollection(item['type'])
            configuration.collections.append(collection)

            for sub_item in item['sub_objects']:
                obj = fabric(item['type'])

                if obj is None:
                    continue
                collection.append(obj)

                obj.collectionName = item['type']
                obj.name = sub_item['name']
                files[obj] = sub_item['file_name']

        self.configuration = configuration
        return configuration

    def object_info(self, obj):
        return parse_object_info.parse(utils.get_obj_file(self.source_code_directory, obj))

    def read_objects_info(self):

        for collection in self.configuration.collections:
            for item in collection:
                self.object_info(item)

    def read_module_info(self, obj):
        pass

    def read_modules_iter(self):

        for collection in self.configuration.collections:
            for obj in collection:

                data_path = os.path.join(utils.get_obj_directory(self.source_code_directory, obj), 'ext')

                for file in utils.find_modules(data_path):
                    module_info = module_parser.parse_file(file)
                    module_info.name = obj.collectionName + '.' + obj.name

                    yield module_info