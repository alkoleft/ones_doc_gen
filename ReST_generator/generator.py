'''
Позволяет создать документацию по код в формате reStructuredText
'''
import os
from ones_parser import parser


def build(source_code_directory):
    output_path = r'F:\tmp\1c-doc'
    if not os.path.exists(output_path):
        os.mkdir(output_path)

    with open(os.path.join(output_path, 'index.rst'), 'w', encoding='utf-8') as index_stream:
        write_header(index_stream, 'Объекты')
        objects = parser.find_objects(source_code_directory)

        write_toctree(index_stream, (item['type'] for item in objects))

    for object_type_info in objects:

        output_type_path = os.path.join(output_path, object_type_info['type'])
        if not os.path.exists(output_type_path):
            os.mkdir(output_type_path)

        with open(os.path.join(output_path, '%s.rst' % object_type_info['type']), 'w', encoding='utf-8') as stream:
            write_header(stream, object_type_info['type'])
            write_toctree(stream, ('%s/%s' %(object_type_info['type'], item['name']) for item in object_type_info['sub_objects']))

        for item in object_type_info['sub_objects']:
            with open(os.path.join(output_type_path, '%s.rst' % item['name']), 'w', encoding='utf-8') as stream:
                obj_info = parser.object_info(source_code_directory, item['file_name'])
                write_header(stream, obj_info['name'] if not obj_info['synonym'] else obj_info['synonym'])
                write_properties(stream, obj_info)


def write_header(stream, text):
    stream.write('\n%s\n%s\n%s\n\n' % (
        '#' * text.__len__(),
        text,
        '#' * text.__len__())
                 )


def write_toctree(stream, items):
    stream.write(
'''

.. toctree::
   :maxdepth: 2

''')

    for item in items:
        stream.write('   %s\n' % item)


def write_properties(stream, properties):
    stream.write(
'''
.. csv-table:: Значения свойств
   :header: "Свойство", "Значение"
   :widths: 10, 30


''')
    for key in properties:
        stream.write('   %s, %s\n' % (key, properties[key]))


def write_method(stream, method_info):

    stream.write(
'''

.. function:: %s(%s)

''' % (method_info.name, method_info.parameters)
    )

    if method_info.description:
        for line in method_info.description.split('\n'):
            stream.write('   %s\n' % line)

    if method_info.parameters:
        stream.write('\n')
        for p in method_info.parameters.split(','):

            stream.write('   :param %s:\n' % p.strip())
