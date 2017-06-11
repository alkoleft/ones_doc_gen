from .base_info import base_info
from enum import Enum


class ModuleInfo:

    def __init__(self):
        self.name = ''
        self.methods = []
        self.vars = []


class MethodType(Enum):
    UNKNOWN = 0
    FUNCTION = 1
    PROCEDURE = 2

class MethodInfo(base_info):

    def __init__(self):
        super().__init__()

        self.type = MethodType.UNKNOWN
        self.parameters = ''
        self.export = False
        self.body = ''

    def set_type(self, type_string):
        if str.lower(type_string) == 'функция':
            self.type = MethodType.FUNCTION
        elif str.lower(type_string) == 'процедура':
            self.type = MethodType.PROCEDURE
        else:
            self.type = MethodType.UNKNOWN

    def __str__(self):
        return self.type.name + ' ' + self.name