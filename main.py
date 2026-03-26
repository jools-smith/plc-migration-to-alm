# This is a sample Python script.
import argparse
import os
from dataclasses import dataclass
from pathlib import Path

from columns import Columns, Product
from program import Program

print(f'program {__name__}')

@dataclass(frozen=True)
class ProgramArgs:
    input_file: Path
    sheet: str
    verbose: bool

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="excel_tool",
        description="Read an Excel sheet and do something useful."
    )

    # Positional or required args
    p.add_argument("input_file", type=Path, help="Path to the Excel file (.xlsx)")

    # Optional args
    p.add_argument("-s", "--sheet", default="Sheet1", help="Excel sheet name (default: Sheet1)")
    p.add_argument("-v", "--verbose", default=False, action="store_true", help="Enable verbose logging")
    return p


def parse_args(argv=None) -> ProgramArgs:
    ns = build_parser().parse_args(argv)

    # Convert Namespace -> dataclass
    return ProgramArgs(
        input_file=ns.input_file,
        sheet=ns.sheet,
        verbose=ns.verbose
    )


def main(argv=None) -> int:
    clear()

    args = parse_args(argv)

    if args.verbose:
        print(f"Args: {args}")

    # Your app logic here:
    # - read Excel
    # - process
    # - write output


    program = Program()

    if not args.input_file.is_file():
        raise FileNotFoundError(f'cannot find {args.input_file}')

    print(f"Reading {args.input_file} sheet={args.sheet}")
    program.load(args.input_file)

    if not program.sheets.__contains__(args.sheet):
        raise Exception(f"Sheet {args.sheet} not found in {args.input_file}")

    for key in program.sheets.get(args.sheet).to_dict(orient='records'):

        prod = Product(
            product_code=key[Columns.SKU.value],
            product_line=key[Columns.PRODUCT_LINE.value],
            suite_name=key[Columns.SUITE_NAME.value],
            suite_version=key[Columns.SUITE_VERSION.value],
            catalog_name=key[Columns.CATALOG_NAME.value],
            catalog_version=key[Columns.CATALOG_VERSION.value]
        )

        print(prod)

    return 0

if __name__ == '__main__':
    SystemExit(main())
    # try:
    #     main()
    #     sys.exit(0)
    # except Exception as e:
    #     print(f'error: {e.__class__.__name__}: {str(e)}')
    #     sys.exit(-1)
    # finally:
    #     pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
