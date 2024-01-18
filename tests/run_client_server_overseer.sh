#!/bin/bash
BASE_DIR="$(dirname "$0")"
. "$BASE_DIR/definitions.sh"

server &
overseer &
client &

wait
