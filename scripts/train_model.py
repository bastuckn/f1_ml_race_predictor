import numpy as np

from src.feature_engineering.build_features import build_feature_table
from src.training.train_model import train_model, save_model
from src.training.evaluate import evaluate

df = build_feature_table()

model, x_test, y_test, feature_list = train_model(df, test_year=2025)

evaluate(model, x_test, y_test)

save_model(model, feature_list)
