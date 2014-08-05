#!/bin/bash

VENV_DIRECTORY="venv"

show_help() {
    echo $0": Creates a venv."
    echo '-h: show this help'
}

venv_create() {
    if [[ -d $VENV_DIRECTORY ]]; then
        echo "Venv already exists, skipping creation"
        exit 0
    else
        echo "Creating venv"
        virtualenv --no-site-packages venv
        echo "Venv successfully created"
    fi
}

while getopts "h" opt; do
    case "$opt" in
    h)
        show_help
        exit 0
        ;;
    esac
done

venv_create
