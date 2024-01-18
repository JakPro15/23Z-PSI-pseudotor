#!/bin/bash
middle_node() {
    cd "$BASE_DIR/../middle_node" || exit 1
    python3 "./middle_node.py" "127.0.0.1" "127.0.0.1" "-t" "$1" "-ss" "$2" "$3"
}

overseer() {
    cd "$BASE_DIR/../overseer" || exit 1
    python "./overseer.py" "127.0.0.1"
}

client() {
    cd "$BASE_DIR/../client" || exit 1
    python "./client.py" "127.0.0.1" "8002" "127.0.0.1"
}

server() {
    cd "$BASE_DIR/../server" || exit 1
    python "./server.py" "127.0.0.1" "8002"
}
