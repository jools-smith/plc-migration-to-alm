from dataclasses import dataclass

from Product import Product
import xml.etree.ElementTree as ET

LHS = "__CDATA_START__"
CDL = "<![CDATA["
RHS = "__CDATA_END__"
CDR = "]]>"

@dataclass
class Suite:
    part_number: str
    name: str
    version: str
    products: list[Product]

    def __hash__(self) -> int:
        return hash(self.part_number)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Suite):
            return NotImplemented
        return self.part_number == other.part_number

    @staticmethod
    def cdata(text):
        return f"{LHS}{text}{RHS}"

    @staticmethod
    def replace_cdata(text):
        return text.replace(LHS, CDL).replace(RHS, CDR)

    def generate_suite_xml(self, root, deployment_state, license_technology, license_generator, license_model):

        suite = ET.SubElement(root, 'suite')

        ET.SubElement(suite, 'name').text = Suite.cdata(self.name)
        ET.SubElement(suite, 'version').text = Suite.cdata(self.version)
        ET.SubElement(suite, 'description').text = Suite.cdata('')
        ET.SubElement(suite, 'state').text = deployment_state

        licenseTechnology = ET.SubElement(suite, 'licenseTechnology')
        primaryKeys = ET.SubElement(licenseTechnology, 'primaryKeys')
        ET.SubElement(primaryKeys, 'name').text = Suite.cdata(license_technology)

        licenseGenerator = ET.SubElement(suite, 'licenseGenerator')
        primaryKeys = ET.SubElement(licenseGenerator, 'primaryKeys')
        ET.SubElement(primaryKeys, 'name').text = Suite.cdata(license_generator)

        ET.SubElement(suite, 'headerResourceBundleKey').text = Suite.cdata('')
        ET.SubElement(suite, 'trailerResourceBundleKey').text = Suite.cdata('')

        products = ET.SubElement(suite, 'products')

        for p in self.products:
            product = ET.SubElement(products, 'product')
            primaryKeys = ET.SubElement(product, 'primaryKeys')
            ET.SubElement(primaryKeys, 'name').text = Suite.cdata(p.name)
            ET.SubElement(primaryKeys, 'version').text = Suite.cdata(p.version)

            ET.SubElement(product, 'count').text = '1'

            licenseModels = ET.SubElement(suite, 'licenseModels')
            licenseModel = ET.SubElement(licenseModels, 'licenseModel')
            primaryKeys = ET.SubElement(licenseModel, 'primaryKeys')
            ET.SubElement(primaryKeys, 'name').text = Suite.cdata(license_model)

        ET.SubElement(suite, 'usedOnDevice').text = 'true'

        productCategory = ET.SubElement(suite, 'productCategory')
        primaryKeys = ET.SubElement(productCategory, 'primaryKeys')
        ET.SubElement(primaryKeys, 'name').text = Suite.cdata(p.product_line)

        ET.SubElement(suite, 'allowDownloadObsoleteFrInAdmin').text = 'false'
        ET.SubElement(suite, 'allowDownloadObsoleteFrInPortal').text = 'false'
        ET.SubElement(suite, 'fnpVersions').text = Suite.cdata('')