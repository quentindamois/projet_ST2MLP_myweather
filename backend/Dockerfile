FROM python:3.14-slim

WORKDIR /app

# install dependencies first (context contains requirements.txt at root)
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# put the Python package inside a subdirectory so that
# `python -m backend.app` works when we later set /app as sys.path
RUN mkdir -p /app/backend
COPY . /app/backend

# keep root of project on PYTHONPATH so 'backend' package is discoverable
WORKDIR /app
EXPOSE 8000

CMD ["python", "-m", "backend.app"]