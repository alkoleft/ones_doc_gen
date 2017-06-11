

from ReST_generator import generator
from ones_parser.parser import Parser

# print(parser.object_info(r'F:\tmp\1c_export_modules\Catalogs\Справочник1.xml'))
# generator.build(r'F:\tmp\1c_export_modules')

parser = Parser(r'F:\tmp\1c_export_modules')
conf = parser.read_structure()
parser.read_objects_info()

with open(r'F:\tmp\1c-doc\methods.rst', 'w', encoding='utf-8') as stream:
    for module_info in parser.read_modules_iter():

        if module_info.methods.__len__() == 0:
            continue
        generator.write_header(stream, module_info.name)
        for method in module_info.methods:
            generator.write_method(stream, method)

print(conf)