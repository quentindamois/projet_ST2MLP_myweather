& "$PSScriptRoot\.venv\Scripts\activate.ps1"
echo "run ruff check --fix"
& "$PSScriptRoot\.venv\Scripts\python" -m ruff check ./training/*.py ./backend/*.py --fix
echo "run ruff format"
& "$PSScriptRoot\.venv\Scripts\python" -m ruff format ./training/*.py ./backend/*.py
echo "run npx eslint"
cd ./frontend
#npx eslint 
cd ../
echo "launch training script"
python ./training/training_script.py
echo "building image"
docker compose -f ./deploy/docker-compose.dev.yml build --no-cache
echo "lauching container"
docker compose -f ./deploy/docker-compose.dev.yml up