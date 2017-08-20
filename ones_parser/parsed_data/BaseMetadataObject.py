class BaseMetadataObject:

    def __init__(self, name = ''):
        self.name = name
        self.synonym = ''
        self.collectionName = ''
        self.properties = None
        self.modules = []


class TableMetaObject(BaseMetadataObject):

    def __init__(self, name=''):
        super().__init__(name)

        self.properties = []


def fabric(type):
    if type in [
        'AccountingRegisters'
        , 'AccumulationRegisters'
        , 'BusinessProcesses'
        , 'CalculationRegisters'
        , 'Catalogs'
        , 'ChartsOfAccounts'
        , 'ChartsOfCalculationTypes'
        , 'ChartsOfCharacteristicTypes'
        , 'CommandGroups'
        , 'CommonAttributes'
        , 'CommonCommands'
        , 'CommonForms'
        , 'CommonModules'
        , 'CommonPictures'
        , 'CommonTemplates'
        , 'Constants'
        , 'DataProcessors'
        , 'DefinedTypes'
        , 'DocumentJournals'
        , 'DocumentNumerators'
        , 'Documents'
        , 'Enums'
        , 'EventSubscriptions'
        , 'ExchangePlans'
        , 'ExternalDataSources'
        , 'FilterCriteria'
        , 'FunctionalOptions'
        , 'FunctionalOptionsParameters'
        , 'HTTPServices'
        , 'InformationRegisters'
        , 'Interfaces'
        , 'Languages'
        , 'Reports'
        , 'Roles'
        , 'ScheduledJobs'
        , 'Sequences'
        , 'SessionParameters'
        , 'SettingsStorages'
        , 'StyleItems'
        , 'Styles'
        , 'Subsystems'
        , 'Tasks'
        , 'WebServices'
        , 'XDTOPackages']:
        return TableMetaObject()

