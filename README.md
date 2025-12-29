Niklas Bastuck
niklas.bastuck@gmail.com

# Formula 1 ML Race Predictor

## Goals of this project:

### Implemented:

- Data ingestion from F1 data sources
- Feature engineering and dataset preparation
- Model training, evaluation, and versioning
- Prediction step and output
- Deployment and remote access on Raspi server via `connect.raspberrypi.com`

### To-Do:

- Background prediction service on a Raspberry Pi
- Persistent storage of predictions
- An API to retrieve the latest predictions
- Hard-code driver lineup for 2026?

# Install Dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Using the Predictor

## Fetch Data using FastF1

Run the script to fetch historical race results, practice sessions, and qualifying data:

Example: latest race

```
python -m scripts/fetch_latest_race.py
```

- This will populate your database with the latest available sessions.

To populate the cache for entire seasons, run for example the following:

```
python3 -m scripts.backfill 2024 2025 R
python3 -m scripts.backfill 2024 2025 Q
```

## Build Feature Table

Create the ML feature table (pre-weekend features only):

```
python3 -m scripts.bootstrap_db
```
and
```
python3 -m scripts.build_features
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
🏎️ Predicted race result for the 2025 Abu Dhabi Grand Prix:

 P Driver            Team  Predicted Pos  Actual Pos  Δ
 1    NOR         McLaren           4.09           3  2
 2    VER Red Bull Racing           4.46           1 -1
 3    RUS        Mercedes           4.54           5  2
 4    ANT        Mercedes           6.42          15 11
 5    PIA         McLaren           6.78           2 -3
 6    LEC         Ferrari           8.80           4 -2
 7    ALO    Aston Martin           9.98           6 -1
 8    HAD    Racing Bulls          10.69          17  9
 9    LAW    Racing Bulls          10.96          18  9
10    GAS          Alpine          12.02          19  9
11    SAI        Williams          12.85          13  2
12    HUL     Kick Sauber          12.88           9 -3
13    OCO    Haas F1 Team          13.24           7 -6
14    BEA    Haas F1 Team          13.37          12 -2
15    HAM         Ferrari          13.64           8 -7
16    TSU Red Bull Racing          14.18          14 -2
17    STR    Aston Martin          14.27          10 -7
18    ALB        Williams          14.56          16 -2
19    COL          Alpine          14.86          20  1
20    BOR     Kick Sauber          15.03          11 -9
```

Feel free to add your own models and code!
