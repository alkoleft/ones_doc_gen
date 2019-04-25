from .BaseMetadataCls import BaseMetadataCls


class RefMeta(BaseMetadataCls):

    def __init__(self, name):
        super.__init__(self, name)

        self.properties = []
        self.tabularSections = []