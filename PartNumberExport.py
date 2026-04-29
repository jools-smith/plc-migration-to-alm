from dataclasses import dataclass


@dataclass()
class PartNumberExport:
    TransactionType:str
    PartNumber:str
    Description:str
    ProductName:str
    ProductVersion:str
    LicenseModel:str
    AvailableForTrial:bool

    def __init__(self, sku, suite_name, suite_description, suite_version, suite_license_model):
        self.TransactionType = 'CreateUpdatePartNumber'
        self.PartNumber = sku
        self.Description = suite_description
        self.ProductName = suite_name
        self.ProductVersion = suite_version
        self.LicenseModel = suite_license_model
        self.AvailableForTrial = False

    @staticmethod
    def get_field_names():
        return [
            "TransactionType",
            "PartNumber",
            "Description",
            "ProductName",
            "ProductVersion",
            "LicenseModel",
            "AvailableForTrial"
        ]
