from enum import Enum


class BaseInfo:
    def __init__(self, name=''):
        self.name = name
        self.description = ''


class ModuleInfo:

    def __init__(self):
        self.name = ''
        self.methods = []
        self.vars = []
        self.file_name = None


class MethodType(Enum):
    UNKNOWN = 0
    FUNCTION = 1
    PROCEDURE = 2


class MethodInfo(BaseInfo):

    def __init__(self):
        super().__init__()

        self.context = None
        self.export = False
        self.type = MethodType.UNKNOWN
        self.parameters = []
        self.parameters_str = ''
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


class VariableInfo(BaseInfo):
    def __init__(self):
        super().__init__()

        self.type = None
        self.export = False


class ParameterInfo(BaseInfo):
    def __init__(self, name, default_value):
        super().__init__(name)

        self.type = None
        self.default_value = default_value
