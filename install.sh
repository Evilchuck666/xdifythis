#!/bin/bash

# Check if we have python3 installed
echo "############################################################";
echo "################# CHECKING SYSTEM PACKAGES #################";
echo "############################################################";
if ! which python3 > /dev/null; then
    echo "";
    echo "Python3 is not installed. Please install it and run this script again.";
    echo "If you use Ubuntu, you can install it with the following command:";
    echo "sudo apt install python3";
    exit 1;
else
    echo "Python3 is already installed.";
fi

# Download and install the latest version of PIP if it is not installed
if ! which pip3 > /dev/null; then
    echo "";
    echo "PIP is not installed. Please install it and run this script again.";
    echo "If you use Ubuntu, you can install it with the following command:";
    echo "sudo apt install python3-pip";
    exit 1;
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
