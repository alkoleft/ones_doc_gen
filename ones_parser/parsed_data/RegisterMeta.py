from .BaseMetadataCls import BaseMetadataCls


class RegisterMeta(BaseMetadataCls):

    def __init__(self, name):
        super.__init__(self, name)

        self.properties = []
        self.dimentions = []