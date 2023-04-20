set -x

python -m alembic upgrade head

python -u flask_app.py &

cd /app/client && npm run develop