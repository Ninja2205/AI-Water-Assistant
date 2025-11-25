#!/usr/bin/env bash
set -e

# Default port and mode
PORT="${PORT:-8000}"
MODE="${LAUNCH_MODE:-api}"

# If using Streamlit, run the dashboard. Otherwise run uvicorn FastAPI app.
if [ "$MODE" = "streamlit" ]; then
  echo "Starting Streamlit on port $PORT"
  exec streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
else
  echo "Starting Uvicorn (FastAPI) on port $PORT"
  exec uvicorn src.api:app --host 0.0.0.0 --port $PORT --proxy-headers
fi
