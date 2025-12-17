from src.feature_engineering.build_features import build_feature_table, save_features

df = build_feature_table()

print(df.isnull().sum())
print(df.describe())

save_features(df)
