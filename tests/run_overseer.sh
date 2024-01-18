#!/bin/bash
BASE_DIR="$(dirname "$0")"
. "$BASE_DIR/definitions.sh"

overseer &

wait
