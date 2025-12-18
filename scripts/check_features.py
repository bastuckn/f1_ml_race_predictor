from src.feature_engineering.build_features import build_feature_table

# Pre-weekend sanity check
df_pre = build_feature_table(include_qualifying=False)
print("Pre-weekend nulls:")
print(df_pre.isnull().sum())

# Post-qualifying sanity check
df_post = build_feature_table(include_qualifying=True)
print("Post-qualifying nulls:")
print(df_post.isnull().sum())
