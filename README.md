Niklas Bastuck
niklas.bastuck@gmail.com

# Formula 1 ML Race Predictor

## Goals of this project:

### Implemented:

- Data ingestion from F1 data sources
- Feature engineering and dataset preparation
- Model training, evaluation, and versioning
- Prediction step and output
- Hard-code driver lineup for 2026 (to bridge the gap for the first race)
- Deployment and remote access on Raspi server via `connect.raspberrypi.com`
- Prediction storage and retrieval functions

# Install Dependencies

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Alternatively, you can run `./scripts/setup/install_dependencies.sh` from the project root.

# Using the Predictor

## Fetch Data using FastF1

Run the script to fetch historical race results, practice sessions, and qualifying data:

Example: latest race

```
python3 -m scripts/fetch_latest_race.py
```

- This will populate your database with the latest available sessions.

To populate the cache for entire seasons, run for example the following:

```
python3 -m scripts.backfill 2024 2025 R
python3 -m scripts.backfill 2024 2025 Q
```

Alternatively, you can run `./scripts/setup/backfill.sh` from the project root.

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

Alternatively, you can run `./scripts/setup/build_features.sh` from the project root.


## Train the Pre-Weekend Model

Train the model using only historical pre-weekend features:

```
python3 -m scripts/train_model.py
```

- Saves a model bundle (e.g., models/race_model_pre_quali.pkl) including:
  - The trained RandomForestRegressor
  - The feature columns used for training (pre_weekend_feature_columns)

Alternatively, you can run `./scripts/setup/train_model.sh` from the project root.

## Predict Race outcome (pre-weekend)

### Next race:

```
python3 -m scripts.predict_next_race <model_path>
```

### Any race:

(This takes only data leading up to this event)

```
python -m scripts.predict_pre_weekend <year> <round> <model_path>
```

Output:

```
🏎️ Predicted race result for the 2025 Abu Dhabi Grand Prix:

 P Driver            Team  Predicted Pos  Actual Pos   Δ
 1    NOR         McLaren           4.41           3   2
 2    RUS        Mercedes           4.73           5   3
 3    ANT        Mercedes           6.15          15  12
 4    PIA         McLaren           6.97           2  -2
 5    VER Red Bull Racing           7.15           1  -4
 6    LEC         Ferrari           8.84           4  -2
 7    ALO    Aston Martin           9.71           6  -1
 8    HAD    Racing Bulls          10.73          17   9
 9    HAM         Ferrari          10.76           8  -1
10    LAW    Racing Bulls          10.88          18   8
11    SAI        Williams          11.55          13   2
12    HUL     Kick Sauber          12.90           9  -3
13    GAS          Alpine          13.11          19   6
14    ALB        Williams          14.04          16   2
15    TSU Red Bull Racing          14.16          14  -1
16    STR    Aston Martin          14.29          10  -6
17    OCO    Haas F1 Team          14.32           7 -10
18    BEA    Haas F1 Team          14.34          12  -6
19    COL          Alpine          14.74          20   1
20    BOR     Kick Sauber          14.80          11  -9
```

## Show a previous prediction

```
python3 -m scripts.show_prediction --next
```

Feel free to contribute your own models and code!

# Running the predictor in the background as a service

You can run the predictor in the background, e.g. on a raspi, so you never forget to run a prediction and it is always ready to be accessed. 

Create the service:

```
sudo nano /etc/systemd/system/f1-predict.service
```

```
[Unit]
Description=F1 Prediction Service
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/f1_ml_race_predictor
ExecStart=/home/pi/f1_ml_race_predictor/.venv/bin/python -m scripts.run_prediction_service models/model.pkl
Restart=always

[Install]
WantedBy=multi-user.target
```

And enable it:

```
sudo systemctl daemon-reexec
sudo systemctl enable f1-predict
sudo systemctl start f1-predict
```
