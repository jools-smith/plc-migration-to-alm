from dataclasses import dataclass


@dataclass
class ProductExport:
    TransactionType:str
    ProductName:str
    ProductVersion:str
    # OldProductName: str
    # OldProductVersion: str
    DeployState:str
    Description:str
    FeatureName:str
    FeatureVersion:str
    FeatureType:str
    Quantity:str
    LicenseTechnology:str
    # HostType: str
    # LicenseGenerator: str
    LicenseModels:str
    # TransactionKeyDefault: str
    # TransactionKeyVirtual: str
    # PackageName: str
    # PackageVersionFormat: str
    # PackageVersion: str
    UsedOnDevice:str
    # UsageModel: str
    ProductLine:str
    # FNPVersion: str
    # HeaderResourceBundleKey: str
    # TrailerResourceBundleKey: str
    # AdminObsoleteFulfillmentDnld: str
    # PortalObsoleteFulfillmentDnld: str
    StartDate:str
    EndDate:str
    EmailTemplate:str

    def __init__(self):
        pass

    def initialize_product_line(self, name, version, product_line):
        self.TransactionType = 'CreateUpdateProduct'
        self.DeployState = 'DRAFT'
        self.Description = ''
        self.FeatureName = ''
        self.FeatureVersion = ''
        self.FeatureType = ''
        self.Quantity = ''
        self.LicenseTechnology = 'FlexNet Licensing'
        self.LicenseModels = 'PLC2'
        self.UsedOnDevice = 'Yes'
        self.ProductName=name
        self.ProductVersion=version
        self.ProductLine=product_line
        self.StartDate = ''
        self.EndDate = ''
        self.EmailTemplate = ''

    def update_as_feature_line(self, name, version, quantity):
        self.FeatureName = name
        self.FeatureVersion = version
        self.FeatureType = 'FIXED'
        self.Quantity = quantity

    @staticmethod
    def get_field_names():
        return [
            "TransactionType",
            "ProductName",
            "ProductVersion",
            # OldProductName: str
            # OldProductVersion: str
            "DeployState",
            "Description",
            "FeatureName",
            "FeatureVersion",
            "FeatureType",
            "Quantity",
            "LicenseTechnology",
            # HostType: str
            # LicenseGenerator: str
            "LicenseModels",
            # TransactionKeyDefault: str
            # TransactionKeyVirtual: str
            # PackageName: str
            # PackageVersionFormat: str
            # PackageVersion: str
            "UsedOnDevice",
            # UsageModel: str
            "ProductLine",
            # FNPVersion: str
            # HeaderResourceBundleKey: str
            # TrailerResourceBundleKey: str
            # AdminObsoleteFulfillmentDnld: str
            # PortalObsoleteFulfillmentDnld: str
            "StartDate",
            "EndDate",
            "EmailTemplate"
        ]
