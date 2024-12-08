#!/bin/bash

ansible=$(command -v ansible)
if [ "$ansible" ]
then
    echo "ERROR! Ansible is already installed."
    exit 1
fi

yum=$(command -v yum)
apt=$(command -v apt)
if [ "$yum" ]
then
    package_manager=$yum
elif [ "$apt" ]
then
    package_manager=$apt
else
    echo "ERROR! Unsupported Linux distribution (must be Debian or Red Hat)."
    exit 1
fi

function install_package {
    while true; do
        read -r -p "Do you wish to install $1? (y/n) " yn
        case $yn in
            [Yy]* ) /usr/bin/sudo "$package_manager" -y install "$1"; break;;
            [Nn]* ) exit 1;;
            * ) echo "Please answer y(es) or n(o).";;
        esac
    done
}

if ! [ "$(command -v python3)" ]
then
    echo "ERROR! Python 3 is not found."
    install_package python3
fi

if ! [ "$(command -v pip3)" ]
then
    echo "ERROR! Python 3 package manager (PIP) is not found."
    install_package python3-pip
fi

python3 -m pip install --user --upgrade pip
python3 -m pip install --user ansible
python3 -m pip install --user ansible-lint
