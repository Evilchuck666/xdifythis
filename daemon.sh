#!/bin/bash

cd ~/xdifythis/ || exit;

echo "Beginning..." > output.log;
echo "Beginning..." > error.log;

while :; do
    date >> output.log;
    date >> error.log;

    sh ~/xdifythis/server.sh;
    sleep 10;
done
