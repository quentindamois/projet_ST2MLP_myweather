import os

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from load_depency import load_model

app = Flask(__name__)
# allow cross-origin calls from the front‑end during development/docker
CORS(app)
model = load_model()
load_dotenv()


@app.get("/health")
def health():
    return {"status": "ok", "stage": os.getenv("MODEL_ALIAS", "Staging")}


@app.post("/predict_temperature")
def predict():
    payload = request.get_json(force=True)
    X = payload["features"]
    preds = model.predict(X)
    return jsonify({"predictions": preds.tolist()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
