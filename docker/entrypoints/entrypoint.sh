#!/usr/bin/env bash

set -e

# If no arguments, drop into a bash shell.
# If arguments are passed and the first argument is "test", run the test suit
# otherwise execute what was passed.
if [[ $# == 0 ]]; then
  /bin/bash
elif [[ $1 == "run-tests" ]]; then
  shift
  source docker/entrypoints/run_tests.sh "$@"
elif [[ $1 == "start-prod-service" ]]; then
  shift
  source docker/files/start-service.sh prod-service "$@"
elif [[ $1 == "start-dev-service" ]]; then
  shift
  source docker/files/start-service.sh dev-service "$@"
else
  exec "$@"
fi