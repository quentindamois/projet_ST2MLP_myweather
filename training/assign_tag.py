import os

import mlflow
from mlflow.tracking import MlflowClient


def main():
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    os.environ["MLFLOW_TRACKING_USERNAME"] = token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token
    client = MlflowClient()
    name = os.environ["MODEL_NAME"]
    alias = os.environ["MODEL_ALIAS"]
    new_alias = os.environ["NEW_MODEL_ALIAS"]

    # we get the info on the history of model
    info_models = client.search_registered_models(filter_string=f"name='{name}'")[0]

    # we get the version correspond to the alias
    version_of_alias = info_models.aliases[alias]

    client.set_registered_model_alias(name, "dev", version_of_alias)

    print(f"Add the alias {new_alias} to {alias} of {name} v{version_of_alias}")


if __name__ == "__main__":
    main()
