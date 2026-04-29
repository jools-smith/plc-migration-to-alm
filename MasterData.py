from dataclasses import dataclass


@dataclass()
class MasterData:
    PRODUCT_CODE: str
    PRODUCT_NAME: str
    EXTERNAL_MODULE_SKU: str
