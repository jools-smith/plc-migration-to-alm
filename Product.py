from dataclasses import dataclass

from Feature import Feature


@dataclass
class Product:
    name: str
    version: str
    product_line: str
    features: list[Feature]
