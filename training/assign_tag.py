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

    # Get registered model
    info_models = client.search_registered_models(filter_string=f"name='{name}'")[0]

    # If alias exists → use it
    if alias in info_models.aliases:
        version = info_models.aliases[alias]
        print(f"Alias {alias} exists → using version {version}")
    else:
        # Otherwise → take latest version
        latest_versions = client.get_latest_versions(name)
        version = latest_versions[0].version
        print(f"Alias {alias} does not exist → using latest version {version}")

    # Set new alias
    client.set_registered_model_alias(name, new_alias, version)

    print(f"Set alias {new_alias} to version {version} of model {name}")


if __name__ == "__main__":
    main()
