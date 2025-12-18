Niklas Bastuck
niklas.bastuck@gmail.com

# Formula 1 ML Race Predictor

## Goals of this project:

### Implemented:

- Data ingestion from F1 data sources
- Feature engineering and dataset preparation
- Model training, evaluation, and versioning

### To-Do:

- Also output actual race result
- Background prediction service on a Raspberry Pi
- Persistent storage of predictions
- An API to retrieve the latest predictions

# Install Dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Using the Predictor

## Fetch Data using FastF1

Run the script to fetch historical race results, practice sessions, and qualifying data:

```
python -m scripts/fetch_latest_race.py
```

- This will populate your database with the latest available sessions.

## Build Feature Table

Create the ML feature table (pre-weekend features only):

```
python -m scripts/build_feature_table.py
```

- Omits current weekend qualifying data (q1_time, q2_time, q3_time, quali_position)
- Computes historical features like driver_avg_finish, team_avg_finish, etc.
- Outputs a table ready for training or prediction.

## Train the Pre-Weekend Model

Train the model using only historical pre-weekend features:

```
python -m scripts/train_model.py
```

- Saves a model bundle (e.g., models/race_model_pre_quali.pkl) including:
  - The trained RandomForestRegressor
  - The feature columns used for training (pre_weekend_feature_columns)

## Predict Race Outcome (Pre-Weekend)

```
python -m scripts/predict_pre_weekend.py <year> <round>
```

### Example:

```
python -m scripts/predict_pre_weekend.py 2025 24
```

Output:

```
I have predicted the following race result for the 2025 Abu Dhabi Grand Prix: 

driver_id         team_id  position_pred
      VER Red Bull Racing       4.678093
      RUS        Mercedes       4.861887
      NOR         McLaren       5.667517
      ANT        Mercedes       7.645915
      PIA         McLaren       8.829029
      LEC         Ferrari       9.559160
      LAW    Racing Bulls       9.836621
      HAD    Racing Bulls      10.011451
      ALO    Aston Martin      10.437706
      GAS          Alpine      12.064814
      HUL     Kick Sauber      12.569693
      SAI        Williams      12.608828
      TSU Red Bull Racing      12.723687
      BEA    Haas F1 Team      12.996972
      STR    Aston Martin      13.133002
      HAM         Ferrari      13.532930
      COL          Alpine      13.711434
      OCO    Haas F1 Team      13.739774
      ALB        Williams      14.047822
      BOR     Kick Sauber      14.811819
```

Feel free to add your own models and code!
