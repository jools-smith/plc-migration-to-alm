from dataclasses import dataclass


@dataclass
class Feature:
    name: str
    description: str
    version: float
    quantity: int
