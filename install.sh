#!/bin/bash

ansible=$(command -v ansible)
if [ $ansible ]
then
    echo "ERROR! Ansible is already installed."
    exit 1
fi

if ! [ $(command -v python3) ]
then
    echo "ERROR! Python 3 is not found."
    exit 1
fi

if ! [ $(command -v pip3) ]
then
    echo "ERROR! Python 3 package manager (PIP) is not found."
    exit 1
fi

python3 -m pip install --upgrade pip
python3 -m pip install --user ansible
python3 -m pip install --user ansible-pylibssh
