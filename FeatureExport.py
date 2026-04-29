from dataclasses import dataclass


@dataclass
class FeatureExport:
    TransactionType:str
    FeatureName:str
    FeatureVersion:float
    VersionFormat:str
    FeatureState:str
    Units:str
    Scale:str
    FeatureDescription:str
    VendorString:str
    Notice:str
    SerialNumber:str
    Counted:str
    Reusable:str
    ClientUniqueness:str
    GroupMask:str

    def __init__(self, name, version, description):
        self.TransactionType = 'CreateUpdateFeature'
        self.FeatureName = name
        self.FeatureVersion = version
        self.VersionFormat = 'FIXED'
        self.FeatureState = 'DRAFT'
        self.Units = ''
        self.Scale = ''
        self.FeatureDescription = description
        self.VendorString = ''
        self.Notice = ''
        self.SerialNumber = ''
        self.Counted = ''
        self.Reusable = ''
        self.ClientUniqueness = ''
        self.GroupMask = ''

    @staticmethod
    def get_field_names():
        return [
        'TransactionType',
        'FeatureName',
        'FeatureVersion',
        'VersionFormat',
        'FeatureState',
        'Units',
        'Scale',
        'FeatureDescription',
        'VendorString',
        'Notice',
        'SerialNumber',
        'Counted',
        'Reusable',
        'ClientUniqueness',
        'GroupMask'
        ]