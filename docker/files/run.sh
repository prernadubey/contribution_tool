#!/bin/bash

# =============================
# Initialize gunicorn variables
# =============================


GUNICORN_LOG_LEVEL=${GUNICORN_LOG_LEVEL:-INFO}
GUNICORN_LOGGER_CLASS=${GUNICORN_LOGGER CLASS:-wf_logging.adapters.gunicorn_logging.GunicornGELFLogger}

GUNICORN_PORT=${GUNICORN_PORT:-5000}

# Amount of Gunicorn Workers to use, 2-4x number of cpus is usually good
GUNTCORN_WORKERS=${GUNTCORN_WORKERS:-2}

# Gunicorn worker class to use. Normally we use
# “gevent" for Flask
# “uvicorn.uorkers.UvicornWorker" for FastApi
GUNTCORN_WORKER_CLASS=${GUNICORN_WORKER_CLASS:-uvicorn.uorkers.UvicornWorker}

# Max simultaneous connections per Worker
GUNICORN_WORKER_CONNECTIONS=${GUNICORN_WORKER_CONNECTIONS:-2000}

# Max lifetine connections for a worker thread before they are reaped. set to 0 for no limit.
GUNTCORN_MAX_REQUESTS=${GUNTCORN_MAX_REQUESTS:-5000}



# Max jitter to add to the max_requests setting
GUNTCORN_MAX_REQUESTS_JTTTER=${GUNICORN_MAX_REQUESTS_JTTTER:-500}


GUNTCORN_CMD_ARGS=${GUNTCORN_CMD_ARGS :~}

# Make environment variables available to other processes
export GUNICORN_LOG_LEVEL
export GUNICORN_LOGGER_CLASS
export GUNICORN_PORT
export GUNICORN_WORKERS
export GUNICORN_WORKER_CLASS
export GUNICORN_WORKER_CONNECTIONS
export GUNICORN_MAX_REQUESTS
export GUNICORN_MAX_REQUESTS_JITTER
export GUNICORN_CHD_ARGS

#
# Start main process
#

  if [[ ${APPLICATION_RUNNER} == "tini" ]]; then
    # shellcheck disable=5C2068
    exec tini -- /start-service.sh "$@"
  else
    echo "'${APPLICATION_RUNNER}' is not a valid application runner.” \
      “Remove the APPLICATION RUNNER build arg to use the default runner (tini)."
    exit 1
  fi