class Transformer:
    @staticmethod
    def clean_data(df, remove_duplicates=True, remove_na=False, normalize_columns=True):
        if normalize_columns:
            df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_", regex=False)
        if remove_duplicates:
            df = df.drop_duplicates()
        if remove_na:
            df = df.dropna()
        return df
