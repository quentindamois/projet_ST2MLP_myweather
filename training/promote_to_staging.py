import os
import json
import sys
import os, mlflow
from mlflow.tracking import MlflowClient

MAE_THRESHOLD = float(os.getenv("MAE_THRESHOLD", "25000"))


def get_latest_metric(metric_history, name):
    """Get the latest metric for a model"""
    history_filtered_metric = list(filter(lambda a: a.key == "mae", metric_history))
    if len(history_filtered_metric) > 0:
        return sorted(history_filtered_metric, key=lambda a: a.timestamp, reverse=True)[
            -1
        ].value
    else:
        return 0


def main():
    mlflow.set_tracking_uri(os.environ["MLFLOW_TRACKING_URI"])
    token = os.environ["MLFLOW_TRACKING_TOKEN"]
    os.environ["MLFLOW_TRACKING_USERNAME"] = token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = token
    client = MlflowClient()
    name = os.environ["MODEL_NAME"]
    alias = os.environ["MODEL_ALIAS"]

    # we get the info on the history of model
    info_models = client.search_registered_models(filter_string=f"name='{name}'")[0]

    # we get the version correspond to the alias
    version_of_alias = info_models.aliases[alias]

    # we look for the name of run corresponding to the model name and the version
    filter_string = f"name='{name}'"
    results_pagelist = client.search_model_versions(filter_string)
    # look among the model with the same name for the one with the correct version
    selected_model_info = list(
        filter(lambda a: a.version == version_of_alias, results_pagelist)
    )[0]
    run_id_of_alias = selected_model_info.run_id

    # We get the mean absolute squared error
    mae = float(
        get_latest_metric(client.get_metric_history(run_id_of_alias, "mae"), "mae")
    )

    passed = mae <= MAE_THRESHOLD
    result = {
        "passed": passed,
        "mae": mae,
        "threshold": MAE_THRESHOLD,
        "model_version": version_of_alias,
        "run_id": run_id_of_alias,
    }
    print(json.dumps(result))
    if not passed:
        sys.exit(2)
    if passed:
        client.set_registered_model_alias(name, "Staging", version_of_alias)
        print(f"Promoted {name} v{version_of_alias} to Staging")


if __name__ == "__main__":
    main()
