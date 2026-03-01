# Running the test suite

The project includes three categories of tests, as requested:

* **unit tests** (Python) – exercise small pieces of logic without external services
* **integration tests** (Python) – spin up the Flask app and hit real endpoints
* **end‑to‑end test** (frontend) – executed with Playwright against the UI

## Python tests

1. make sure the virtual environment is active (`.venv\Scripts\activate.ps1`).
2. install the test dependencies if you haven't already:

```powershell
pip install -r requirements.txt
```

`pytest` is included in `requirements.txt`.

3. run all Python tests from the repository root:

```powershell
# from project root
pytest
```

If you only want unit or integration tests, you can use markers:

```powershell
pytest tests/unit
pytest tests/integration
```

The fixture in `tests/integration/test_api.py` automatically patches the model so that
no DVC or MLflow backend is required.

## Frontend end‑to‑end test

The UI tests use Playwright. From the `frontend/` directory:

```sh
npm install            # first time only
npx playwright install  # install browsers
npm run test:e2e        # runs the e2e suite
```

The single test exercises the weather form and intercepts the network
call; it will fail if the component mistakenly displays a promise ("[object Promise]").

## Notes

* There are no dedicated JavaScript unit tests yet; you can add them under
  `frontend/src/__tests__` or similar and wire them into `package.json`.

* The front‑end fetch URL is controlled by the `VITE_BACKEND_URL` environment
  variable.  During development you can set it to `http://localhost:8001` (the
  port exposed by the backend compose service).  In Docker builds the compose
  file already sets this variable so the static assets point at the correct
  host.

* The backend enables CORS (via `flask_cors.CORS`) so that the UI running on
  port 8080 can call the API on 8001 without the browser complaining.  This is
  already handled in `backend/app.py` and requires `flask-cors` in
  `requirements.txt` (it is already listed).
  port exposed by the backend compose service).  In Docker builds the compose
  file already sets this variable so the static assets point at the correct
  host.
* Python tests assume the repository root is on `PYTHONPATH` (running `pytest`
  from the root accomplishes that).
* You can run the entire suite with `.
  lauch_dev.ps1` after modifying the script to include `pytest` if required.

Happy testing!