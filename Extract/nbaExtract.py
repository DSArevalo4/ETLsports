import pandas as pd
from Config.configuraciones import Config

class Extractor:
    def __init__(self, file_path=None):
        self.file_path = file_path or Config.INPUT_PATH

    def extract(self):
        df = pd.read_excel(self.file_path)
        return df
