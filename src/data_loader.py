import pandas as pd

def load_data(path):
    df = pd.read_csv(path, encoding="latin-1")
    df = df[['v1', 'v2']]
    df.columns = ['label', 'message']
    return df


def encode_labels(df):
    df['label'] = df['label'].map({'spam': 1, 'ham': 0})
    return df