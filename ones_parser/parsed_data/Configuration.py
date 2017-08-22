from .BaseMetadataObject import BaseMetadataObject


class Configuration(BaseMetadataObject):

    def __init__(self):
        super().__init__(self)
        self.collections = []
        self.data_path = None
