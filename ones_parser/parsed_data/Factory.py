from . import BaseMetadataCls

__table_types__ = None
__all_types__ = None

def __init__():
    global __table_types__, __all_types__

    if not __all_types__ is None:
        return
    __table_types__ = [
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
        , 'XDTOPackages']

    __all_types__ = [item for item in __table_types__]


def meta_collection(type):
    __init__()
    global __all_types__

    if type in __all_types__:
        return BaseMetadataCls.MetadataCollection(type)

def object(type, name):
    __init__()
    if type in __table_types__:
        obj = BaseMetadataCls.TableMetaObject(name)
        obj.typeName = type

        return obj

