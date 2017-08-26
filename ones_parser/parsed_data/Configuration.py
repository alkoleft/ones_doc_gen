from .BaseMetadataCls import BaseMetadataCls


class Configuration(BaseMetadataCls):

    def __init__(self):
        super().__init__(self)
        self.collections = []
        self.data_path = None
