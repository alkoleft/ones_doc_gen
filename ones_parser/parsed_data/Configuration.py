from .BaseMetadataObject import BaseMetadataObject


class Configuration(BaseMetadataObject):

    def __init__(self):
        self.collections = []

class MetadataCollection(list):

    def __init__(self, name =''):
        list.__init__(self)
        self.name = name