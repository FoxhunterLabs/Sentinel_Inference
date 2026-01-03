#!/usr/bin/env bash
set -euo pipefail

export SENTINEL_RELOAD=true
export SENTINEL_UVICORN_LOG_LEVEL=info

python -m app.main
