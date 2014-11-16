#!/bin/sh

VBoxManage -v foo >/dev/null 2>&1 || {
    echo >&2 "Ensure Virtual Box is installed and in the path.  Aborting.";
    open 'https://www.virtualbox.org/wiki/Downloads';
    exit 1;
}

vagrant -v foo >/dev/null 2>&1 || {
    echo >&2 "Ensure vagrant is installed and in the path.  Aborting.";
    open 'https://www.vagrantup.com/downloads.html';
    exit 1;
}

vagrant plugin list | grep 'hostmanager' &> /dev/null

if [ $? != 0 ]; then
    echo "Ensure vagrant-hostmanager plugin for vagrant is installed.  Aborting.";
    echo "Run this: vagrant plugin install vagrant-hostmanager";
    exit 1;
fi

echo "You're all set."