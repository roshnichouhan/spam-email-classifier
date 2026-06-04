def create_features(df):
    df['length'] = df['message'].apply(len)
    df['words'] = df['message'].apply(lambda x: len(x.split()))
    df['digits'] = df['message'].apply(lambda x: sum(c.isdigit() for c in x))
    df['upper'] = df['message'].apply(lambda x: sum(c.isupper() for c in x))

    df['free'] = df['message'].str.lower().str.contains("free").astype(int)
    df['win'] = df['message'].str.lower().str.contains("win").astype(int)
    df['click'] = df['message'].str.lower().str.contains("click").astype(int)

    return df