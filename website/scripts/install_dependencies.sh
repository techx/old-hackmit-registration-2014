#!/bin/bash

VENV_ACTIVATE=./venv/bin/activate
APPLICATION_ROOT=./application
EXCLUDE_DIRECTORIES="config static templates tests"
PIP_DEPENDENCIES_FILENAME=requirements.txt
BOWER_DEPENDENCIES_FILENAME=bower.json

show_help() {
    echo $0": Installs python (pip) and js (bower) dependencies."
    echo '-h: show this help'
}

install() {
    for file in *; do
        if [[ $file = $PIP_DEPENDENCIES_FILENAME ]]; then
            echo "Installing python dependencies for $(basename $(pwd))"
            pip install -r $PIP_DEPENDENCIES_FILENAME
        fi
        if [[ $file = $BOWER_DEPENDENCIES_FILENAME ]]; then
            echo "Installing js dependencies for $(basename $(pwd))"
            bower install
        fi
    done
}
 
recursive_install() {
    shopt -s nullglob

    cd $1

    install

    for directory in *; do
        if [[ -d $directory ]]; then
            included=true
            for exclude in $EXCLUDE_DIRECTORIES; do
                if [[ $directory = $exclude ]]; then
                    included=false
                fi
            done
            if [[ $included = true ]]; then
                recursive_install $directory
            fi
        fi
    done
    
    cd ..
}

full_dependency_install() {
    recursive_install $APPLICATION_ROOT

    #pip freeze > $PIP_DEPENDENCIES_FILENAME
}

while getopts "h" opt; do
    case "$opt" in
    h)
        show_help
        exit 0
        ;;
    esac
done

source $VENV_ACTIVATE

full_dependency_install
