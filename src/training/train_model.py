from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.training.split import time_based_split

def train_model(df, test_year=2025):
    # Create mixed training data

    # Time-based split
    train_df, test_df = time_based_split(df, test_year)

    # Define target and features
    y_train = train_df["position"]
    y_test = test_df["position"]

    omitted_columns = ["position", "points", "q1_time", "q2_time", "q3_time", "quali_position", "grid"]

    x_train = train_df.drop(columns=omitted_columns)
    x_test = test_df.drop(columns=omitted_columns)

    feature_list = x_train.columns.tolist()  # <-- save the exact training columns

    print("Training on features: \n", x_test.columns)

    model = RandomForestRegressor(
        n_estimators=400,
        max_depth=14,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(x_train, y_train)

    return model, x_test, y_test, feature_list


def save_model(model, feature_list, path="models/race_position_model_" + datetime.today().strftime('%Y-%m-%d') + ".pkl"):
    # Save model + feature names
    joblib.dump({
        "model": model,
        "features": feature_list  # <-- save the exact training columns
    }, path)
