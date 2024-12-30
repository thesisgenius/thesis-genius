#!/usr/bin/env bash

## Logging Functions
function info() {
    echo -e "${GREEN}[INFO]${RESET} $1"
}

function warn() {
    echo -e "${YELLOW}[WARN]${RESET} $1"
}

function error() {
    echo -e "${RED}[ERROR]${RESET} $1" >&2
}
