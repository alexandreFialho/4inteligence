#!/bin/sh

./wait-for-it.sh $POSTGRES_SERVER:$POSTGRES_PORT

alembic upgrade head

uvicorn api.main:app --reload --host 0.0.0.0 --port 8000