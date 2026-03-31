import pandas

class Table:
    def __init__(self):
        self.columns = []
        self.sheets = None
        self.path = None


    def add_column(self, column) -> Table:
        self.columns.append(column)
        return self

    def load(self, path) -> Table:

        if not path.is_file():
            raise FileNotFoundError(f'cannot find {path}')

        self.path = path

        self.sheets = pandas.read_excel(self.path, sheet_name=None, engine="openpyxl")

        return self


    def extract_sheet(self, sheet) -> list:

        if not self.sheets.__contains__(sheet):
            raise Exception(f"Sheet {sheet} not found in {self.path}")

        data = []

        for key in self.sheets.get(sheet).to_dict(orient='records'):
            if len(self.columns) > 0:
                data.append([key[x] for x in self.columns])
            else:
                data.append(key)

        return data