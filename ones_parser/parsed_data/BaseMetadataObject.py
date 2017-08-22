import os


class BaseMetadataObject:

    def __init__(self, name = ''):
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


class TableMetaObject(BaseMetadataObject):

    def __init__(self, name=''):
        super().__init__(name)

        self.properties = []


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
