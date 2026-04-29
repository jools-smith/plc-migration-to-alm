from dataclasses import dataclass


@dataclass()
class CatalogItem:
    SYSTEM_ID: int
    ID: str
    NAME: str
    TYPE: str
    CREATED: str
    MANUFACTURER: str
    PRODUCT_LINE: str


