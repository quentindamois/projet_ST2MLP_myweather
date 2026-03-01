import pandas as pd
import numpy as np
import pytest

import training.training_script as ts


def test_load_data_monkeypatch(tmp_path, monkeypatch):
    # simulate dvc.api.read returning CSV content
    csv = "Humidity_pct,Wind_Speed_kmh,Temperature_C\n0.1,1.0,10\n0.2,2.0,20"
    monkeypatch.setattr(ts.dvc.api, "read", lambda path: csv)
    X, y = ts.load_data()
    assert isinstance(X, pd.DataFrame)
    assert list(X.columns) == ["Humidity_pct", "Wind_Speed_kmh"]
    assert isinstance(y, pd.Series)
    assert y.tolist() == [10, 20]


def test_train_model_returns_pipeline(monkeypatch):
    # patch load_data to use a dataset large enough for KNeighborsRegressor(n_neighbors=5)
    # With 80/20 split, 10 samples -> 8 training + 2 test samples, which is enough for 5 neighbors
    X = pd.DataFrame({
        "Humidity_pct": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        "Wind_Speed_kmh": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    })
    y = pd.Series([10, 12, 14, 16, 18, 20, 22, 24, 26, 28])
    monkeypatch.setattr(ts, "load_data", lambda: (X, y))
    model, mae = ts.train_model()
    # pipeline should have 'knn' step
    assert hasattr(model, "predict")
    assert mae >= 0


def test_build_postgres_uri_env(monkeypatch):
    from backend.load_depency import _build_postgres_uri
    # no environment variables -> default string
    uri = _build_postgres_uri()
    assert uri.startswith("postgresql+psycopg2://")
    # with custom variables
    monkeypatch.setenv("POSTGRES_USER", "u")
    monkeypatch.setenv("POSTGRES_PASSWORD", "p")
    monkeypatch.setenv("POSTGRES_HOST", "h")
    monkeypatch.setenv("POSTGRES_PORT", "1234")
    monkeypatch.setenv("POSTGRES_DB", "db")
    uri2 = _build_postgres_uri()
    assert "u:p@h:1234/db" in uri2
