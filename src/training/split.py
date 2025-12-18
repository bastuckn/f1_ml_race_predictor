def time_based_split(df, test_year):
    """
    Train on all data before test_year.
    Test on test_year only.
    Don't shuffle. 
    """
    train_df = df[df["year"] < test_year]
    test_df = df[df["year"] == test_year]

    return train_df, test_df
