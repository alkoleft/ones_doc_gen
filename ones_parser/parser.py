import os

from ones_parser.module_parser.module_info import ModuleInfo
from ones_parser.xml_info_parser import parse_object_info
from . import utils
from .module_parser.parser import Parser as mParser
from .parsed_data.BaseMetadataObject import fabric
from .parsed_data.Configuration import Configuration, MetadataCollection

MODULES = 1
OBJECTS = 2


class Parser:
    """
    Выполняет разбор выгрузки исходников 1с.
    Получает информацию о:
    
       * Струкруре выгрузки
       * Объектах метаданных
       * Структуре модулей
       
    """
    def __init__(self, source_code_directory):
        self.source_code_directory = source_code_directory
        self.configuration = None
        self.module_parser = None

    def read_structure(self):
        """
        Читает структуру выгрузки.
        Возвращает информацию о имеющихся объектах 1с, на основании иерархии каталогов

        :return: Иерархическое описание структуры объектов конфигурации
        """

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

                data_path = os.path.join(utils.get_obj_directory(self.source_code_directory, obj), 'ext')

                for file in utils.find_modules(data_path):
                    module_info = ModuleInfo()
                    module_info.name = obj.collectionName + '.' + obj.name
                    module_info.file_name = file
                    obj.modules.append(module_info)

        self.configuration = configuration
        return configuration

    def object_info(self, obj):
        """
        Читает информацию о объекте из XML-файла описания

        :param obj: Описание объекта
        :return: Описание свойств объекта
        """

        obj.properties = parse_object_info.parse(self.get_file_name(obj))
        return obj.properties

    def read_objects_info(self):
        """
        Читает информацию о всех объектах конфигурации из XML-файлов описания

        :return: None
        """
        for collection in self.configuration.collections:
            for item in collection:
                self.object_info(item)

    def read_modules_info_iter(self):
        """
        Читает информацию о модулях объекта

        :return: Информация о модулях
        """

        if self.module_parser is None:
            self.module_parser = mParser()

        for collection in self.configuration.collections:
            for obj in collection:

                data_path = os.path.join(utils.get_obj_directory(self.source_code_directory, obj), 'ext')
                for module_info in obj.modules:
                    self.module_parser.parse_module(module_info, os.path.join(data_path, module_info.file_name))
                    yield module_info

    def get_file_name(self, obj):
        return utils.get_obj_file(self.source_code_directory, obj)
