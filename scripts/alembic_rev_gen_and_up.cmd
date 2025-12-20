cd ..
.venv\Scripts\python.exe -m alembic -c alembic.ini revision --autogenerate -m "auto"
.venv\Scripts\python.exe -m alembic -c alembic.ini upgrade head