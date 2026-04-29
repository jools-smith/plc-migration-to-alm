from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProgramArgs:
    root: Path
    catalog : str
    catalog_sheet : str
    excel : str
    excel_sheet: str
    feature_sheet : str
    verbose: bool
