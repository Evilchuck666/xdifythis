#!/bin/bash

# Check if lock file exists
if [ -f "lock" ]; then
    echo "";
    echo "The bot is already running.";
    echo "If you want to start it again, delete the lock file or wait until the script finishes.";
    echo "";
    exit 1;
fi

# Create lock file
touch lock;

# Run the bot
echo "###################################################################";
echo "########################### RUNNING BOT ###########################";
echo "###################################################################";
echo "";

python3 bot.py >> output.log 2>> error.log;

rm -rf lock;
