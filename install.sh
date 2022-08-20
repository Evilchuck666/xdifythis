#!/bin/bash

# Check if we have python3 installed
echo "############################################################";
echo "################# CHECKING SYSTEM PACKAGES #################";
echo "############################################################";
if ! which python3 > /dev/null; then
    echo "Python3 is not installed. Please install it and run this script again.";
    echo "If you use Ubuntu, you can install it with the following command:";
    echo "sudo apt install python3";
    exit 1;
else
    echo "Python3 is already installed.";
fi

# Check if we have wget installed
if ! which wget > /dev/null; then
    echo "Wget is not installed. Please install it and run this script again.";
    echo "If you use Ubuntu, you can install it with the following command:";
    echo "sudo apt install wget";
    exit 1;
else
    echo "Wget is already installed.";
fi

# Download and install the latest version of PIP if it is not installed
if ! which pip3 > /dev/null; then
    wget https://bootstrap.pypa.io/get-pip.py;
    python3 get-pip.py;
    rm get-pip.py;
else
    echo "PIP is already installed.";
    echo "";
fi

# Install bot dependencies
echo "###########################################################";
echo "############### INSTALLING BOT DEPENDENCIES ###############";
echo "###########################################################";
echo "Installing bot dependencies...";
echo "";
pip3 install -r requirements.txt
