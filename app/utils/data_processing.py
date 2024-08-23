import pandas as pd

def sanitize_data(filepath):
    data = pd.read_csv(filepath)
    data.dropna(inplace=True)
    sanitized_filepath = filepath.replace('.csv', '_sanitized.csv')
    data.to_csv(sanitized_filepath, index=False)
    return sanitized_filepath

