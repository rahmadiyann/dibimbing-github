#!/bin/bash
if [[   $(docker ps --filter name=dataeng* -aq) ]]; then
    echo 'Stopping Container...'
    docker ps --filter name=dataeng* -aq | xargs docker stop
    echo 'All Container Stopped...'
else
    echo "All Cleaned UP!"
fi