#!/bin/bash
BASE_DIR="$(dirname "$0")"
. "$BASE_DIR/definitions.sh"

server &
overseer &
client &
middle_node 0.5 400 500

wait
