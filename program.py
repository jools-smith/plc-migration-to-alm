import pandas
import openpyxl

class Program:

    def __init__(self):
        self.sheets={}
        pass

    def load(self, path):
        self.sheets = pandas.read_excel(path, sheet_name=None, engine="openpyxl")

    def get(self):
        return self.sheets

