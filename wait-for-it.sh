#!/bin/bash

# wait-for-it.sh

# Usage: wait-for-it.sh host:port [-- command ...]
# Wait for the specified host and port to be ready, then execute the command.

TIMEOUT=60 # Augmenter le timeout
WAIT_HOSTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    -*)
      break
      ;;
    *)
      WAIT_HOSTS+=("$1")
      ;;
  esac
  shift
done

for WAIT_HOST in "${WAIT_HOSTS[@]}"; do
  HOST=${WAIT_HOST%%:*}
  PORT=${WAIT_HOST##*:}

  if [[ "$HOST" == "$PORT" ]]; then
    PORT=80
  fi

  # Wait for the host and port to be ready
  echo "Waiting for $WAIT_HOST to be available..."
  nc -z -v -w $TIMEOUT $HOST $PORT
  if [[ $? -ne 0 ]]; then
    echo "ERROR: $WAIT_HOST is not available, exiting."
    exit 1
  fi
  echo "$WAIT_HOST is ready!"
done

# Si des commandes supplémentaires sont fournies, les exécuter
if [[ $# -gt 0 ]]; then
  exec "$@"
fi
