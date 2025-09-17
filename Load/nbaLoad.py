import sqlite3
import pandas as pd

class Loader:
    def __init__(self, data_frame):
        self.df = data_frame

    def to_csv(self, output_path):
        self.df.to_csv(output_path, index=False)

    def to_sqlite(self, db_path, table_name):
        conn = sqlite3.connect(db_path)
        self.df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
