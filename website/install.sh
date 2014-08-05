#!/bin/bash

show_help() {
    echo $0": Full install script:"
    echo '-Installs bower globally'
    echo '-Creates a venv'
    echo '-Installs python and js dependencies' 
    echo 'Options:'
    echo '-h: show this help'
}

install() {
    ./scripts/install_bower.sh
    ./scripts/create_venv.sh
    ./scripts/install_dependencies.sh 
}


while getopts "h" opt; do
    case "$opt" in
    h)
        show_help
        exit 0
        ;;
    esac
done

install

echo ""
echo "Installation complete."
echo "Make sure you activate the venv with 'source venv/bin/activate'!"
