'''
Модуль разбора исходников 1с
'''
import re


from .parsed_data.module_info import MethodInfo, ModuleInfo


def parse_file(file_name):
    '''
    Разбирает файл, возвращает информацию о методах и переменных
    :param file_name: str имя файла
    :return: 
    '''

    with open(file_name, 'r', encoding='utf-8') as stream:
        module_info = parse_module(stream)
        stream.close()

    return module_info


def parse_module(stream):
    '''
    Разбирает поток, возвращает информацию о методах и переменных
    :param stream: поток 
    :return: 
    '''
    text = stream.read()

    module_info = ModuleInfo()
    for var in find_vars(text):
        module_info.vars.append(var)

    for method in find_methods(text):
        module_info.methods.append(method)

    return module_info

def find_vars(text):
    var_pattern = re.compile(r'Перем\s+(.+)\s+Экспорт')
    result = var_pattern.finditer(text)
    for match in result:

        yield match[0]


def find_methods(text):
    module_pattern = re.compile(
        r'(^(\/\/.*$\n)*)[\n\s]*(^&[а-яА-Я]+$)?[\n\s]*^\s*(Функция|Процедура)(.+?)\((.*?)\)\s*(Экспорт)?([\S\s]+?)(КонецФункции|КонецПроцедуры)', re.IGNORECASE | re.MULTILINE)
    result = module_pattern.finditer(text)

    comment_pattern = re.compile(r'\s*\/\/\s*')
    for match in result:

        m = MethodInfo()
        m.name = match.group(5)
        m.description = comment_pattern.sub('\n', match.group(1)).strip()
        m.set_type(match.group(4))
        m.parameters = match.group(6)
        m.body = match.group(0)
        yield m
