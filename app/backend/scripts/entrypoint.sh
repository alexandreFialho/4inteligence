#!/usr/bin/env bash

./scripts/wait-for-it.sh $POSTGRES_SERVER:$POSTGRES_PORT

alembic upgrade head

if [ "$ENV" = "development" ]; then

    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
fi

exec "$@"