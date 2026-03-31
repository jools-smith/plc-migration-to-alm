# This is a sample Python script.
import argparse
import json
import os
from dataclasses import dataclass, asdict
from pathlib import Path

from table import Table

print(f'program {__name__}')

@dataclass(frozen=True)
class ProgramArgs:
    root: Path
    catalog : str
    catalog_sheet : str
    excel : str
    excel_sheet: str
    verbose: bool

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="excel_tool",
        description="Read an Excel sheet and do something useful."
    )

    # Positional or required args
    p.add_argument("--root", default="C:\\Users\\juliansmith\\OneDrive - Flexera, Inc\\Assignments\\PLC Migration\\assessment", type=Path, help="Path root directory")

    p.add_argument("--catalog", default="INST-SearchCatalogItem.xlsx", help="Catalog items (.xlsx)")
    p.add_argument("--catalog-sheet", default="Sheet1", help="Catalog sheet name (default: Sheet1)")
    p.add_argument("--excel", default="PLC_SKU_Mapping-Master.xlsx", help="Excel file (.xlsx)")
    p.add_argument("--excel-sheet", default="MasterData", help="Excel sheet name (default: Sheet1)")
    p.add_argument("-v", "--verbose", default=False, action="store_true", help="Enable verbose logging")
    return p


def parse_args(argv=None) -> ProgramArgs:
    ns = build_parser().parse_args(argv)

    # Convert Namespace -> dataclass
    return ProgramArgs(
        root=ns.root,
        catalog=ns.catalog,
        catalog_sheet=ns.catalog_sheet,
        excel=ns.excel,
        excel_sheet=ns.excel_sheet,
        verbose=ns.verbose
    )

@dataclass()
class CatalogItem:
    SYSTEM_ID: int
    ID: str
    NAME: str
    TYPE: str
    CREATED: str
    MANUFACTURER: str
    PRODUCT_LINE: str

@dataclass()
class MasterData:
    PRODUCT_CODE: str
    PRODUCT_NAME: str
    EXTERNAL_MODULE_SKU: str

@dataclass
class Feature:
    name: str
    version: str

@dataclass
class Product:
    name: str
    version: str
    product_line: str
    features: list[Feature]

@dataclass
class Suite:
    part_number: str
    name: str
    version: str
    products: list[Product]

def main(argv=None) -> int:
    clear()

    args = parse_args(argv)

    if args.verbose:
        print(f"Args: {args}")

    if not args.root.is_dir():
        raise FileNotFoundError(f'cannot find {args.root}')

    path = args.root / args.catalog
    catalog_items = []
    catalog = Table().load(path).extract_sheet(args.catalog_sheet)
    for o in catalog:
        catalog_items.append(CatalogItem(
            SYSTEM_ID=o["SYSTEM_ID"],
            ID=o["ID"],
            NAME=o["NAME"],
            TYPE=o["TYPE"],
            CREATED=o["CREATED"],
            MANUFACTURER=o["MANUFACTURER"],
            PRODUCT_LINE=o["PRODUCT_LINE"])
        )

    path = args.root / args.excel
    master_data_items = []
    master_data = Table().load(path)
    for o in master_data.extract_sheet(args.excel_sheet):
        master_data_items.append(MasterData(
            PRODUCT_CODE=o["Product__r.ProductCode"],
            PRODUCT_NAME=o["Product__r.Name"],
            EXTERNAL_MODULE_SKU=o["External_Module__r.Part_Number__c"])
        )

    required_part_numbers = set()
    for o in master_data.extract_sheet("RequiredProductCodes"):
        required_part_numbers.add(o["Product__r.ProductCode"])

    data = {}
    for o in master_data_items:
        key = o.PRODUCT_CODE

        if not data.__contains__(o.PRODUCT_CODE):
            data[key] = Suite(part_number=key, name=o.PRODUCT_NAME, version="Subscription", products=[])

        suite = data[key]

        for cat in filter(lambda x : x.ID == o.EXTERNAL_MODULE_SKU, catalog_items):
            suite.products.append(Product(name=cat.NAME, version=cat.ID, product_line=cat.PRODUCT_LINE, features=[]))

    with open(args.root / "pcs-products.json", "w", encoding="utf-8") as file:
        jstr = json.dumps({k: asdict(v) for k, v in data.items() if required_part_numbers.__contains__(k)}, indent=2)

        file.write(jstr)
        print(jstr)




    return 0

if __name__ == '__main__':
    SystemExit(main())

