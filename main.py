# This is a sample Python script.
import csv
import json
import os
import xml.etree.ElementTree as ET
from dataclasses import asdict
from pathlib import Path

from CatalogItem import CatalogItem
from Constants import Constants
from Feature import Feature
from FeatureData import FeatureData
from FeatureExport import FeatureExport
from MasterData import MasterData
from PartNumberExport import PartNumberExport
from Product import Product
from ProductExport import ProductExport
from Suite import Suite
from table import Table

print(f'program {__name__}')


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main(argv=None) -> int:
    clear()

    args_root = Path("c:\\working\\python\\PLC\\data")

    path = args_root / "INST-SearchCatalogItem.xlsx"
    catalog_items = []
    for o in Table().load(path).extract_sheet("Sheet1"):
        catalog_items.append(CatalogItem(
            SYSTEM_ID=o["SYSTEM_ID"],
            ID=o["ID"],
            NAME=o["NAME"],
            TYPE=o["TYPE"],
            CREATED=o["CREATED"],
            MANUFACTURER=o["MANUFACTURER"],
            PRODUCT_LINE=o["PRODUCT_LINE"])
        )

    path = args_root / "PLC_SKU_Mapping-Master.xlsx"
    master_data_items = []
    for o in  Table().load(path).extract_sheet("MasterData"):
        master_data_items.append(MasterData(
            PRODUCT_CODE=o["Product__r.ProductCode"],
            PRODUCT_NAME=o["Product__r.Name"],
            EXTERNAL_MODULE_SKU=o["External_Module__r.Part_Number__c"])
        )

    required_part_numbers = set()
    for o in Table().load(path).extract_sheet("RequiredProductCodes"):
        required_part_numbers.add(o["Product__r.ProductCode"])

    path = args_root / "PLC_SKU_Mapping-Master.xlsx"
    feature_items = []
    features = Table().load(path)
    for o in features.extract_sheet("Catalog-Feature Mapping-Master"):
        feature_items.append(FeatureData(
            CATALOG_ITEM_ID=o["Catalog Item ID"],
            FEATURE_NAME=o["Feature Name"],
            FEATURE_DESCRIPTION=o["Feature Description"],
            VERSION=o["Version"],
            UNITS=o["Units In Catalog Item"])
        )

    features_per_catalog = {}
    products = {}
    features = {}

    suites = dict()
    for o in master_data_items:
        key = o.PRODUCT_CODE

        if not suites.__contains__(o.PRODUCT_CODE):
            suites[key] = Suite(part_number=key, name=o.PRODUCT_NAME, version=Constants.SuiteVersion, products=[])

        suite = suites[key]

        for cat in filter(lambda x : x.ID == o.EXTERNAL_MODULE_SKU, catalog_items):

            if not features_per_catalog.__contains__(cat.ID):
                features_per_catalog[cat.ID] = []

                for feature in filter(lambda x : x.CATALOG_ITEM_ID == cat.ID, feature_items):
                    feat = Feature(
                        name=feature.FEATURE_NAME,
                        description=feature.FEATURE_DESCRIPTION,
                        version=feature.VERSION,
                        quantity=feature.UNITS)

                    key = feat.name + " | " + str(feat.version)

                    if not features.__contains__(key):
                        features[key] = feat

                    features_per_catalog[feature.CATALOG_ITEM_ID].append(feat)

            prod = Product(
                name=cat.NAME,
                version=cat.ID,
                product_line=cat.PRODUCT_LINE,
                features=features_per_catalog[cat.ID])

            key = prod.name + " | " + prod.version

            if not products.__contains__(key):
                products[key] = prod

            suite.products.append(prod)

    with open(args_root / "pcs-products.json", "w", encoding="utf-8") as file:
        jstr = json.dumps({k: asdict(v) for k, v in products.items()}, indent=2)
        file.write(jstr)

    with open(args_root / "pcs-suites.json", "w", encoding="utf-8") as file:
        jstr = json.dumps({k: asdict(v) for k, v in suites.items() if required_part_numbers.__contains__(k)}, indent=2)
        file.write(jstr)

    print(f"there were {len(suites.keys())} suites {len(catalog_items)} products found")

    with open(args_root / "part-numbers-demo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=PartNumberExport.get_field_names())
        writer.writeheader()

        for k, v in suites.items():
            if required_part_numbers.__contains__(k):
                item = PartNumberExport(
                    sku=v.part_number,
                    suite_name=v.name,
                    suite_version=v.version,
                    suite_description=v.name + " | " + Constants.SuiteLicenseModel,
                    suite_license_model=Constants.SuiteLicenseModel)
                writer.writerow(asdict(item))

    with open(args_root / "features-demo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FeatureExport.get_field_names())
        writer.writeheader()

        for o in features.values():
            item = FeatureExport(name=o.name, version=o.version, description=o.description)
            writer.writerow(asdict(item))

    with open(args_root / "products-demo.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ProductExport.get_field_names())
        writer.writeheader()

        for o in products.values():
            item = ProductExport()
            item.initialize_product_line(
                name=o.name,
                version=o.version,
                product_line=o.product_line)
            writer.writerow(asdict(item))

            for feat in o.features:
                item.update_as_feature_line(feat.name, feat.version, feat.quantity)
                writer.writerow(asdict(item))

    root = ET.Element('suites', xmlns="urn:com.macrovision:flexnet/operations/exportimport")

    for k, v in suites.items():
        if required_part_numbers.__contains__(k):
            v.generate_suite_xml(root,
                                 deployment_state='DRAFT',
                                 license_technology=Constants.ProductLicenseTechnology,
                                 license_generator = Constants.ProductLicenseGenerator,
                                 license_model = Constants.ProductLicenseModel)

    tree = ET.ElementTree(root)

    xml_content = Suite.replace_cdata(ET.tostring(root,
                                                  short_empty_elements=False,
                                                  encoding="unicode"))

    with open(args_root / "output.xml", "w", encoding="utf-8") as f:
        f.write(xml_content)

    return 0

if __name__ == '__main__':
    SystemExit(main())

