#!/bin/sh
set -e

# Run migrations
uv run alembic upgrade head

# Start app
uv run python ivy/main.py