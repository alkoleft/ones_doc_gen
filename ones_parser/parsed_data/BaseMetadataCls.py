import os
from ones_parser.module_parser import parser as moduleParser


class BaseMetadataCls:

    def __init__(self, name):
        self.owner = None
        self.name = name
        self.synonym = ''
        self.typeName = ''
        self.properties = None
        self.modules = []

    def get_data_path(self):
        if self.owner is None:
            return self.data_path if hasattr(self, 'data_path') else None
        else:
            return os.path.join(self.owner.get_data_path(), self.name)

    def read_modules(self):

        path = os.path.join(self.get_data_path(), 'ext')

        for item in self.modules:
            moduleParser.parse_module(item, os.path.join(path, item.name + '.bsl'))

class TableMetaObject(BaseMetadataCls):

    def __init__(self, name=''):
        super().__init__(name)

        self.properties = []


class RefMetaObject(TableMetaObject):

    def __init__(self, name=''):
        super.__init__(self, name)



class DocumentMeta(BaseMetadataCls):

    def __init__(self, name):
        super.__init__(self, name)

        self.properties = []
        self.tabularSections = []


class MetadataCollection(list):

    def __init__(self, name =''):
        list.__init__(self)
        self.name = name
        self.owner = None

    def get_data_path(self):
        if self.owner is None:
            return self.data_path if hasattr(self, 'data_path') else None
        else:
            return os.path.join(self.owner.get_data_path(), self.name)
