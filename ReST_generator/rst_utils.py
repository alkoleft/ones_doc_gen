import os

from ones_parser import utils


def write_header(stream: object, text: str):
    stream.write('\n%s\n%s\n%s\n\n' % (
        '#' * text.__len__(),
        text,
        '#' * text.__len__())
                 )


def write_toctree(stream, items) -> None:
    stream.write(
        '''
        
        .. toctree::
           :maxdepth: 2
        
        ''')

    for item in items:
        stream.write('   %s\n' % item)


def write_properties(stream, properties):
    if not properties or len(properties) == 0:
        return
    write_table_header(stream, 'Значения свойств', '"Свойство", "Значение"', '10, 30')

    for key in properties:
        stream.write('   %s, %s\n' % (key, properties[key]))


def write_method(stream, method_info):
    stream.write(
        '''
        
        .. function:: %s(%s)
        
        ''' % (method_info.name, method_info.parameters_str)
    )

    flags = []
    if method_info.export:
        flags.append('Экспорт')

    if method_info.context:
        flags.append(method_info.context)

    if flags:
        stream.write('   %s\n\n' % ' '.join(['``%s``' % flag for flag in flags]))

    if method_info.description:
        for line in method_info.description.split('\n'):
            stream.write('   %s\n' % line)

    if method_info.parameters:
        stream.write('\n')
        for p in method_info.parameters:

            line = '   :param %s: ' % p.name.strip()
            stream.write(line)
            write_multi_line_text(stream, p.description, len(line))

            if p.type:
                stream.write('   :type %s: %s\n' % (p.name.strip(), p.type))


def write_multi_line_text(stream, text, indent):
    if text:
        prefix = None
        for line in text.split('\n'):
            if not prefix:
                stream.write('%s\n' % line)
                prefix = ' ' * indent
            else:
                stream.write('%s%s\n' % (prefix, line))
    else:
        stream.write('\n')


def write_attributes(stream, attributes):
    if not attributes or len(attributes) == 0:
        return

    write_table_header(stream, _('Attributes'), '"%s", "%s"' % (_('Name'), _('Synonym')), '10, 30')

    for attr in attributes:
        stream.write('   %s, %s\n' % (attr['name'], attr['synonym']))


def write_table_header(stream, caption, headers, widths):
    stream.write(
        '''
.. csv-table:: %s 
   :header: %s
   :widths: %s

''' % (caption, headers, widths))


def write_modules(parser, output):
    utils.create_if_not_exists(output)

    for module_info in parser.read_modules_info_iter():

        output_path = os.path.join(output, module_info.name.replace('.', os.path.sep))
        utils.create_if_not_exists(output_path)

        file_name = output_path + module_info.file_name + '.rst'
        with open(file_name, 'w', encoding='utf-8') as stream:

            write_header(stream, module_info.name)
            print(file_name)
            for method in module_info.methods:
                write_method(stream, method)
