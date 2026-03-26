from dataclasses import dataclass
from enum import Enum


class Columns(Enum):
    SKU = "SalesForce Product Code"
    PRODUCT_LINE = "Catalog Product Line"
    SUITE_NAME = "Catalog Item Name"
    SUITE_VERSION = "Catalog Item Version"
    CATALOG_NAME = "Catalog Item Id"
    CATALOG_VERSION = "Catalog Item Id Version"


@dataclass(frozen=True)
class Product:
    product_code: str       # SalesForce product code
    product_line: str
    suite_name: str         # PLC1.0 catalog item id
    suite_version: str         # PLC1.0 catalog item id
    catalog_name: str         # PLC1.0 catalog item id
    catalog_version: str       # PLC1.0 catalog item name