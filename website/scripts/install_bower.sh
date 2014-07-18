#!/bin/bash

show_help() {
    echo $0": Installs bower globally."
    echo '-h: show this help'
}

bower_install() {
    echo "Checking for bower"
    if [[ ! -z "$(which bower)" ]]; then
        echo "Bower already installed, skipping"
        exit 0
    else
        echo "Installing bower"
        npm install -g bower
        if [[ $? -ne 0 ]]; then
            sudo npm install -g bower
        fi
        echo "Bower successfully installed"
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

bower_install
