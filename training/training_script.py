import os
import json
import time
import mlflow
import mlflow.sklearn
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

from dotenv import load_dotenv


MODEL_NAME = os.getenv("MODEL_NAME", "weather-model")
DEV_ENV = os.getenv("DEV_ENV", False) # environment value used to determine if we are testing the application localy
if DEV_ENV == "True":
    DEV_ENV = True



def train_model():
    X, y = make_classification(n_samples=2000, n_features=10, random_state=42)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=200, l1_ratio=0.9, C=0.9, solver="saga")
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    return model, acc

def main():

    if not(DEV_ENV):
        tracking_uri = os.environ["MLFLOW_TRACKING_URI"]
        token = os.environ["MLFLOW_TRACKING_TOKEN"]
        mlflow.set_tracking_uri(tracking_uri)
        os.environ["MLFLOW_TRACKING_USERNAME"] = token
        os.environ["MLFLOW_TRACKING_PASSWORD"] = token

        model, acc = train_model()

        run_name = f"candidate-{int(time.time())}"
        with mlflow.start_run(run_name=run_name) as run:
            mlflow.log_metric("accuracy", float(acc))
            mlflow.log_param("model_type", "logreg")
            mlflow.log_param("data_version", os.getenv("DATA_VERSION","dvc:unknown"))
            mlflow.sklearn.log_model(model, artifact_path="model")
            # Register model
            model_uri = f"runs:/{run.info.run_id}/model"
            mv = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
            out = {"run_id": run.info.run_id, "accuracy": float(acc), "model_version": mv.version}
            print(json.dumps(out))
    else:
        model, acc = train_model()
        print(f"model accuracy : {acc}")
        with open('../backend/dev_model.pkl','wb') as f:
            pickle.dump(model, f)

if __name__ == "__main__":
    main()