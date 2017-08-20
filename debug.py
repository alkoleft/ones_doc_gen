

from ReST_generator import generator
from ones_parser.parser import Parser
from ones_parser.module_parser.parser import Parser as mParser

# print(parser.object_info(r'F:\tmp\1c_export_modules\Catalogs\Справочник1.xml'))
# generator.build(r'F:\tmp\1c_export_modules')

parser = Parser(r'F:\tmp\1c_export_modules')

m_parser = mParser()
m_parser.parse_comment(None,
'''
// Определить объекты метаданных, в модулях менеджеров которых ограничивается возможность 
// редактирования реквизитов при групповом изменении.
//
// Параметры:
//   Объекты - Соответствие - в качестве ключа указать полное имя объекта метаданных,
//                            подключенного к подсистеме "Групповое изменение объектов". 
//                            Дополнительно в значении могут быть перечислены имена экспортных функций:
//                            "РеквизитыНеРедактируемыеВГрупповойОбработке",
//                            "РеквизитыРедактируемыеВГрупповойОбработке".
//                            Каждое имя должно начинаться с новой строки.
//                            Если указана пустая строка, значит в модуле менеджера определены обе функции.
//
''')
# conf = parser.read_structure()
# parser.read_objects_info()
#
# with open(r'F:\tmp\1c-doc\methods.rst', 'w', encoding='utf-8') as stream:
#     for module_info in parser.read_modules_iter():
#
#         if module_info.methods.__len__() == 0:
#             continue
#         generator.write_header(stream, module_info.name)
#         for method in module_info.methods:
#             generator.write_method(stream, method)
#
# print(conf)