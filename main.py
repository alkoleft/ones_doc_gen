# -*- coding: utf-8 -*-

import gettext
import os

import ones_parser.xml_info_parser.parse_object_info as xmlParser
from ReST_generator import generator
from ones_parser.parser import Parser

lang_dir = os.path.abspath(os.path.join(os.curdir, 'lang'))
os.environ['LANGUAGE'] = 'ru_RU'
gettext.install('messages', lang_dir)

source_code_directory = r'F:\tmp\1c_export_modules'
print(_('Parse config files'))
parser = Parser(source_code_directory)
cfg = parser.read_structure()
parser.read_objects_info()

print(_('Build documentation'))
generator.build(parser, r'F:\tmp\1c-doc')
