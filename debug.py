import os
from ones_parser.parser import Parser
from ones_parser.xml_info_parser import parse_object_info
# print(parser.object_info(r'F:\tmp\1c_export_modules\Catalogs\Справочник1.xml'))
# generator.build(r'F:\tmp\1c_export_modules')


dump_path = r'F:\tmp\1c_export_modules'
# parser = Parser(dump_path)
# parser.read_structure()

info = parse_object_info.parse_configuration_info(os.path.join(dump_path, 'configuration.xml'))

for item in info['child_objects']:
    print('%s: %s' % (item['type'], item['name']))