#!/usr/bin/env bash

set -euo pipefail

GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-INFO}
GUNICORN_PORT=${GUNICORN_PORT:-5000}

# Amount of Gunicorn Workers to use, 2-4x number of cpus is usually good
GUNICORN_WORKERS=${GUNTCORN_WORKERS:-2}

# Gunicorn worker class to use. Normally we use
# “gevent" for Flask
# “uvicorn.uorkers.UvicornWorker" for FastApi
GUNICORN_WORKER_CLASS=${GUNICORN_WORKER_CLASS:-uvicorn.workers.UvicornWorker}

# Max simultaneous connections per Worker
GUNICORN_WORKER_CONNECTIONS=${GUNICORN_WORKER_CONNECTIONS:-2000}

# Max lifetine connections for a worker thread before they are reaped. set to 0 for no limit.
GUNICORN_MAX_REQUESTS=${GUNTCORN_MAX_REQUESTS:-5000}

# Max jitter to add to the max_requests setting
GUNICORN_MAX_REQUESTS_JITTER=${GUNICORN_MAX_REQUESTS_JTTTER:-500}

if [[ $1 == "prod-service" ]]; then

    gunicorn \
    "components.controller.fastapi.main:create_component()" \
    -b ":${GUNICORN_PORT}" \
    -w "${GUNICORN_WORKERS}" \
    -k "${GUNICORN_WORKER_CLASS}" \
    --log-level="${GUNICORN_LOG_LEVEL}" \
    --worker-connections="${GUNICORN_WORKER_CONNECTIONS}" \
    --max-requests="${GUNICORN_MAX_REQUESTS}" \
    --max-requests-jitter="${GUNICORN_MAX_REQUESTS_JITTER}"
elif [[ $1 == "dev-service" ]]; then

  python -m uvicorn components.controller.fastapi._devel:component --log-level "${GUNICORN_LOG_LEVEL:-info}" \
   --host 0.0.0.0 --port ${GUNICORN_PORT} --reload
fi