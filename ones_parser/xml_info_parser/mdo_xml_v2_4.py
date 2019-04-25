from . import utils
from lxml import etree


ns={
    'mdc': "http://v8.1c.ru/8.3/MDClasses",
    'app': "http://v8.1c.ru/8.2/managed-application/core",
    'cfg': "http://v8.1c.ru/8.1/data/enterprise/current-config",
    'cmi': "http://v8.1c.ru/8.2/managed-application/cmi",
    'ent': "http://v8.1c.ru/8.1/data/enterprise",
    'lf': "http://v8.1c.ru/8.2/managed-application/logform",
    'style': "http://v8.1c.ru/8.1/data/ui/style",
    'sys': "http://v8.1c.ru/8.1/data/ui/fonts/system",
    'v8': "http://v8.1c.ru/8.1/data/core",
    'v8ui': "http://v8.1c.ru/8.1/data/ui",
    'web': "http://v8.1c.ru/8.1/data/ui/colors/web",
    'win': "http://v8.1c.ru/8.1/data/ui/colors/windows",
    'xen': "http://v8.1c.ru/8.3/xcf/enums",
    'xpr': "http://v8.1c.ru/8.3/xcf/predef",
    'xr': "http://v8.1c.ru/8.3/xcf/readable",
    'xs':"http://www.w3.org/2001/XMLSchema" ,
    'xsi':"http://www.w3.org/2001/XMLSchema-instance"}

def parse(root):
    '''

    :param file:
    :return:
    '''
    root = root.find('./*')
    info = read_base_info(root)

    for node in root.findall('./mdc:ChildObjects/mdc:Attribute', ns):
        info['attributes'].append(get_properties(node))
    return info


def parse_configuration_info(root):
    root = root.find('./*')
    info = read_base_info(root)
    child_objects = []
    for node in root.findall('./mdc:ChildObjects/*', ns):
        child_objects.append({
            'type': utils.without_namespace(node.tag),
            'name': node.text
        })

    info['child_objects'] = child_objects

    return info

def read_base_info(root):
    info = {
        'uuid':'',
        'properties': {'name': '', 'synonym': ''}
    }

    info['uuid'] = root.attrib['uuid']
    get_properties(root, info['properties'])

    if info['properties']['synonym'] is None or info['properties']['synonym'] == '':
        info['properties']['synonym'] = info['properties']['name']

    return info


def get_properties(root, info=None):
    '''

    :param root:
    :param info:
    :return:
    '''
    if info is None:
        info = {}

    for node in root.findall('./mdc:Properties/*', ns):
        content_node = node.find('.//v8:content', ns)
        info[utils.without_namespace(node.tag).lower()] = node.text if content_node is None else content_node.text

    return info
