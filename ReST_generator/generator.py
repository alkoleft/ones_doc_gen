'''
Позволяет создать документацию по код в формате reStructuredText
'''
import os

from ones_parser import utils
from . import rst_utils


def build(parser, output_path):
    '''
    Выполяет генерацию документации кода
    На основании выгрузки исходников 1с(в иерархическом формате)
    Формирует описание в формате reStructuredText

    Генерит:
       * Описание структуры
       * Описание обектов метаданных
       * Описание модулей

    :param parser: парсер каталога исходников, файлов выгрузки 1с
    :param str output_path: выходной каталог, в нем будут сформированы файлы документации
    :return:
    '''

    cfg = parser.configuration

    utils.create_if_not_exists(output_path)

    build_main_index(cfg, output_path)

    for collection in cfg.collections:

        output_type_path = os.path.join(output_path, collection.name)
        utils.create_if_not_exists(output_type_path)

        build_collection_index(collection.name, collection.name, collection, output_type_path)

        for item in collection:
            build_item_docs(parser, item, os.path.join(output_type_path, '%s' % item.name))

def build_main_index(cfg, output_path):

    with open(os.path.join(output_path, 'index.rst'), 'w', encoding='utf-8') as index_stream:
        rst_utils.write_header(index_stream, 'Объекты')
        rst_utils.write_toctree(index_stream, (item.name for item in cfg.collections))


def build_collection_index(name, synonym, items, output_path):
    with open(os.path.join(output_path, 'index.rst'), 'w', encoding='utf-8') as stream:
        rst_utils.write_header(stream, synonym)
        rst_utils.write_toctree(stream, (item.name for item in items))


def build_item_docs(parser, item, output_path):

    utils.create_if_not_exists(output_path)

    with open(os.path.join(output_path, 'index.rst'), 'w', encoding='utf-8') as stream:
        obj_info = parser.object_info(item)
        rst_utils.write_header(stream, obj_info['properties']['synonym'])

        rst_utils.write_attributes(stream, obj_info['attributes'])

        rst_utils.write_properties(stream, obj_info['properties'])

        rst_utils.write_toctree(stream, (m.name for m in item.modules), True)

    for module in parser.read_modules(item):
        write_module_info(output_path, module)

def write_module_info(output, module):

    utils.create_if_not_exists(output)

    file_name = os.path.join(output, module.name + '.rst')
    with open(file_name, 'w', encoding='utf-8') as stream:

        rst_utils.write_header(stream, _(module.name))

        for method in module.methods:
            rst_utils.write_method(stream, method)
