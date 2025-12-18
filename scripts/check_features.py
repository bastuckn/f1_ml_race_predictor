from src.feature_engineering.build_features import build_feature_table

# Pre-weekend sanity check
df = build_feature_table()
print("Pre-weekend nulls:")
print(df.isnull().sum())
