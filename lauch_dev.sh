./venv/Script/activate.bat
ruff check ./training/* ./backend/*
ruff format ./training/* ./backend/*
npx eslint yourfile.js
python ./training/training_script.py
docker-compose build -f ./deploy/docker-compose.dev.yml --no-cache --parallel