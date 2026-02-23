import os
import mlflow
import mlflow.pyfunc
import pickle
from dotenv import load_dotenv

ENV_DEV = os.getenv("DEV_ENV", False)
if ENV_DEV == "True":
    ENV_DEV = True
    load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME", "weather-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Staging")


def load_model_staging_or_production():
    """Load a model from the dagshub repository"""
    tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    mlflow.set_tracking_uri(tracking_uri)
    os.environ["MLFLOW_TRACKING_USERNAME"] = token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token
    uri = f"models:/{MODEL_NAME}/{MODEL_STAGE}"
    return mlflow.pyfunc.load_model(uri)


def load_model_dev():
    """load a trained model during training"""
    with open("dev_model.pkl", "rb") as f:
        model = pickle.load(f)
    return model


def load_model():
    print(f"ENV_DEV : {ENV_DEV}")
    if ENV_DEV:
        res = load_model_dev()
    else:
        res = load_model_staging_or_production()


def _build_postgres_uri() -> str:
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        return db_url

    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "postgres")
    host = os.environ.get("POSTGRES_HOST", "localhost")
    port = os.environ.get("POSTGRES_PORT", "5432")
    name = os.environ.get("POSTGRES_DB", "taskmanager")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
