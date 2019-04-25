import os
from lxml import etree
from  . import mdo_xml_v2_4


def parse(file):
    return execute_by_version(file, 'parse')


def parse_configuration_info(file):
    return execute_by_version(file, 'parse_configuration_info')


def execute_by_version(file, method_name):
    if not os.path.exists(file):
        raise Exception('File "%s" not found' % file)
    tree = etree.parse(file)
    root = tree.getroot()

    if root.attrib['version'] == '2.4':
        method = getattr(mdo_xml_v2_4, method_name)
        return method(root)
    else:
        raise Exception('MDO. Not support format')
