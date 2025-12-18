from src.feature_engineering.build_features import build_feature_table

# Pre-weekend sanity check
df_pre = build_feature_table(
print("Pre-weekend nulls:")
print(df_pre.isnull().sum())
