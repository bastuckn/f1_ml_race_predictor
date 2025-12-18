from datetime import datetime
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

from src.training.split import time_based_split

QUALI_FEATURES = [
    "quali_position",
    "quali_gap_to_pole",
    "driver_avg_quali_pos",
    "team_avg_quali_pos",
]

def prepare_training_data(df):
    """
    Create a mixed dataset:
    - Rows with qualifying features
    - Rows without qualifying features (NaNs)
    """

    df_with_quali = df.copy()

    df_no_quali = df.copy()
    df_no_quali[QUALI_FEATURES] = np.nan

    combined_df = pd.concat([df_with_quali, df_no_quali], ignore_index=True)

    return combined_df


def train_model(df, test_year=2025):
    # Create mixed training data
    df = prepare_training_data(df)

    # Time-based split
    train_df, test_df = time_based_split(df, test_year)

    # Define target and features
    y_train = train_df["position"]
    y_test = test_df["position"]

    x_train = train_df.drop(columns=["position", "points"])
    x_test = test_df.drop(columns=["position", "points"])

    model = RandomForestRegressor(
        n_estimators=400,
        max_depth=14,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(x_train, y_train)

    return model, x_test, y_test


def save_model(model, path="models/race_position_model_" + datetime.today().strftime('%Y-%m-%d') + ".pkl"):
    joblib.dump(model, path)
