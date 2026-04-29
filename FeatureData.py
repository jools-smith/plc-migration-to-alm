from dataclasses import dataclass


@dataclass()
class FeatureData:
    CATALOG_ITEM_ID: str
    FEATURE_NAME: str
    FEATURE_DESCRIPTION: str
    VERSION: float
    UNITS: int
