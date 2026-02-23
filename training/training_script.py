import dvc.api
import os
from io import StringIO
import json
import time
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import StandardScaler
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.neighbors import KNeighborsRegressor
from dotenv import load_dotenv

# Source - https://stackoverflow.com/a/76764193 for loading the model
# Posted by davemb83
# Retrieved 2026-02-22, License - CC BY-SA 4.0


ENV_DEV = os.getenv("DEV_ENV", True)
if ENV_DEV == "False":
    ENV_DEV = False
else:
    load_dotenv()


MODEL_NAME = os.getenv("MODEL_NAME", "weather-model")


def load_data():
    """This function load the csv from data folder"""
    contents = dvc.api.read(path="data/weather_data.csv")
    df = pd.read_csv(StringIO(contents))
    X_name_column = ["Humidity_pct", "Wind_Speed_kmh"]
    y_name_column = "Temperature_C"
    return df[X_name_column], df[y_name_column]


def train_model():
    X, y = load_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print(f"creating the pipeline")
    pipeline_model = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("knn", KNeighborsRegressor()),
        ]
    )
    print(f"Training the pipeline")
    pipeline_model.fit(X_train, y_train)
    print(f"Training the model")
    preds = pipeline_model.predict(X_test)
    print(f"Computing the error of the pipeline")
    mae = mean_absolute_error(y_test, preds, multioutput="uniform_average")
    return pipeline_model, mae


def main():

    if not (ENV_DEV):
        tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
        token = os.environ["MLFLOW_TRACKING_TOKEN"]
        mlflow.set_tracking_uri(tracking_uri)
        os.environ["MLFLOW_TRACKING_USERNAME"] = token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = token

        model, mae = train_model()

        run_name = f"candidate-{int(time.time())}"
        with mlflow.start_run(run_name=run_name) as run:
            mlflow.log_metric("mae", float(mae))
            mlflow.log_param("model_type", "logreg")
            mlflow.log_param("data_version", os.getenv("DATA_VERSION", "dvc:unknown"))
            mlflow.log_param(
                "git commit", os.getenv("GIT_COMMIT_HASH", "commit:unknown")
            )
            mlflow.log_params(model.get_params())
            mlflow.sklearn.log_model(model, artifact_path="model")
            # Register model
            model_uri = f"runs:/{run.info.run_id}/model"
            mv = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
            out = {
                "run_id": run.info.run_id,
                "mae": float(mae),
                "model_version": mv.version,
            }
    else:
        model, mae = train_model()
        print(f"Starting the saving of the model")
        with open("./backend/dev_model.pkl", "wb") as f:
            pickle.dump(model, f)
        print(f"the saved model")


if __name__ == "__main__":
    main()
