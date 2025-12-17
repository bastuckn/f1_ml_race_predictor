import pandas as pd

def encode_categoricals(df):
    return pd.get_dummies(
        df,
        columns=["driver", "team", "circuit"],
        drop_first=True
    )
