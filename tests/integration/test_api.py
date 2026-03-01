import pytest
import numpy as np
from backend import app as flask_app


class DummyModel:
    def predict(self, X):
        # simply return sum of features for each row
        return np.sum(X, axis=1)


@pytest.fixture(autouse=True)
def patch_model(monkeypatch):
    # always use dummy model for predict
    monkeypatch.setattr("backend.load_depency.load_model", lambda: DummyModel())
    yield


@pytest.fixture

def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as c:
        yield c


def test_health_endpoint(client):
    rv = client.get("/health")
    assert rv.status_code == 200
    data = rv.get_json()
    assert data["status"] == "ok"
    assert "stage" in data


def test_predict_temperature(client):
    payload = {"features": [[1, 2], [3, 4]]}
    rv = client.post("/predict_temperature", json=payload)
    assert rv.status_code == 200
    data = rv.get_json()
    # DummyModel sums rows: [3,7]
    assert data["predictions"] == [3, 7]
