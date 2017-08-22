"""
Модуль разбора исходников 1с
"""
import re

from ones_parser.module_parser.module_info import MethodInfo, ModuleInfo, ParameterInfo
from . import utils


class Parser:

    def parse_module(self, module_info, file_name):
        with open(file_name, 'r', encoding='utf-8') as stream:
            self.parse_stream(module_info, stream)
            stream.close()

    def parse_file(self, file_name):
        """
        Разбирает файл, возвращает информацию о методах и переменных

        :param file_name: str имя файла
        :return:
        """

        with open(file_name, 'r', encoding='utf-8') as stream:
            module_info = ModuleInfo()
            self.parse_stream(module_info, stream)
            stream.close()

        return module_info

    def parse_stream(self, module_info, stream):
        """
        Разбирает поток, возвращает информацию о методах и переменных

        :param stream: поток
        :return:
        """
        text = stream.read()

        for var in self.find_vars(text):
            module_info.vars.append(var)

        for method in self.find_methods(text):
            module_info.methods.append(method)

        return module_info

    def find_vars(self, text):
        """
        Извлекает описание переменных модуля

        :param text: Текст модуля
        :return:
        """

        var_pattern = re.compile(r'Перем\s+(.+)\s+Экспорт')

        result = var_pattern.finditer(text)
        for match in result:
            yield match[0]

    def find_methods(self, text):
        """
        Извлекает описание методов модуля

        :param text: Текст модуля
        :return:
        """

        method_pattern = re.compile(
            r'(^&[а-яА-Я]+$)?'  # 1. Контекст выполнения
            r'(^(\/\/.*$\n)*)'  # 2. Комментарий
            r'[\n\s]*'  # -  Возможный разрыв (пустые строки)
            r'(^&[а-яА-Я]+$)?'  # 4. Контекст выполнения
            r'[\n\s]*'  # -  Возможный разрыв (пустые строки)
            r'^\s*(Функция|Процедура)'  # 5. Тип метода
            r'(.+?)'  # 6. Имя метода
            r'\((.*?)\)'  # 7. Переменные
            r'\s*(Экспорт)?'  # 8. Экспорт
            r'([\S\s]+?)'  # 9. Тело метода
            r'(КонецФункции|КонецПроцедуры)'  # 10.Конец метода
            , re.IGNORECASE | re.MULTILINE)

        result = method_pattern.finditer(text)

        for match in result:
            m = MethodInfo()
            m.context = match.group(4) if match.group(1) is None else match.group(0)
            m.export = not match.group(8) is None
            m.name = match.group(6)

            m.set_type(match.group(5))
            m.parameters = Parser.parse_parameters(match.group(7))
            m.parameters_str = match.group(7)
            m.body = match.group(10)

            self.parse_comment(m, match.group(2))
            yield m

    def parse_comment(self, m, comment):
        """

        :param MethodInfo m: Информация о методе
        :param comment: Текст комментария
        :return:
        """

        if not comment:
            return False

        comment = (re.sub(r'\s*\/\/', '\n', comment))

        return self.parse_standard_comment(m, comment) or \
               self.parse_raw_comment(m, comment)



        # m.description = re.sub(r'\s*\/\/', '\n', comment)

    def parse_raw_comment(self, m, comment):
        m.description = comment
        pass

    def parse_standard_comment(self, m, comment):

        def parse_parameters_description(parameters, comment):

            indents = utils.text_indents(comment)

            indent = 0
            start_pos = None
            end_pos = comment.__len__()
            for _indent in indents:
                if not _indent['isEmpty']:
                    if start_pos is None:
                        indent = _indent['indent']
                        start_pos = _indent['start']

                    elif _indent['indent'] <= indent:
                        end_pos = _indent['start']

            comment = comment[start_pos: end_pos]
            parameter_description_start = \
                r'^%s([_0-9а-яА-Я]+)(\s*-\s*([_0-9а-яА-Я., ]+))?\s*-\s*([\s\S]+?)\n' % (' ' * indent)

            parameters_desc = []
            for match in re.finditer(parameter_description_start, comment, re.MULTILINE):
                parameters_desc.append({
                    'name': match.group(1),
                    'type': match.group(3),
                    'description-start': match.regs[4][0],
                    'start': match.regs[0][0],
                    'description': match.group(4)
                })
            count = parameters_desc.__len__()
            for index in range(0, count):
                if index == count - 1:
                    parameters_desc[index]['description'] = \
                        utils.clear_indent(comment[parameters_desc[index]['description-start']:])
                else:
                    parameters_desc[index]['description'] = \
                        utils.clear_indent(
                            comment[parameters_desc[index]['description-start']: parameters_desc[index + 1]['start']])

                print('========================')
                print(parameters_desc[index]['name'])
                print(parameters_desc[index]['type'])
                print(parameters_desc[index]['description'])

                p = None

                for _p in parameters:
                    if _p.name == parameters_desc[index]['name']:
                        p = _p
                        break
                if p:
                    p.description = parameters_desc[index]['description']
                    p.type = parameters_desc[index]['type']

        blocks = []
        prev_block = None
        i = None
        new_block = False
        for i in utils.text_indents(comment):
            match = re.match(r'^[\t ]*([ \tа-яА-Я]+):?\s*$', comment[i['start']:i['end']])
            if match:
                i['title'] = match.group(1)
                new_block = True

            if prev_block is not None \
                    and not i['isEmpty'] \
                    and i['indent'] <= prev_block['indent']:
                new_block = True

            if new_block:
                new_block = False
                blocks.append(i)
                if not prev_block is None:
                    prev_block['block_end'] = i['start']
                    print(prev_block)
                prev_block = i

        if not prev_block is None:
            prev_block['block_end'] = i['start']
            print(prev_block)

        # start = 0
        # end = len(comment)
        # groups = []
        # for match in re.finditer(r'^([ \tа-яА-Я]+):?\s*$', comment, re.MULTILINE|re.IGNORECASE):
        #     if len(groups):
        #         groups[len(groups) - 1].append(match.regs[0][0])
        #     groups.append([match.group(1).strip(), match.regs[0][0], match.regs[0][1]])
        #
        # if len(groups):
        #     groups[len(groups) - 1].append(end)
        # else:
        #     print('wazaaaa')
        # print(groups)

        # params_string = 'параметры'
        # result_string = 'возвращаемое значение'
        #
        # good = False
        # for group in groups:
        #     if group[0].lower() in [result_string, params_string]:
        #         good = True
        #         break
        #
        # if not good:
        #     return False
        #
        # description = comment[:groups[0][1]]
        # for group in groups:
        #     if 'параметры' == group[0].lower():
        #         parse_parameters_description(m.parameters, comment[group[2]:group[3]])
        #     else:
        #         description = description + comment[group[2]:group[3]]
        #
        # m.description = description
        # return True
        params_string = 'параметры'
        result_string = 'возвращаемое значение'

        good = False
        for group in blocks:
            if group['title'].lower() in [result_string, params_string]:
                good = True
                break

        if not good:
            return False

        description = comment[:blocks[0]['start']]
        for group in blocks:
            if 'параметры' == group['title'].lower():
                parse_parameters_description(m.parameters, comment[group['end']:group['block_end']])
            else:
                description = description + comment[group['start']:group['block_end']]

        m.description = description
        return True

    @staticmethod
    def parse_parameters(parameters_string):
        result = []
        for match in re.findall(r'([а-яА-Я0-9_a-zA-Z]+)(\s*=\s*([^,]*))?', parameters_string):
            result.append(ParameterInfo(match[0], match[2]))

        return result
