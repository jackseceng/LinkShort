#!/bin/sh

if [ -f "/secretVol/secrets" ]; then
    echo "Loading secrets from /secretVol/secrets"
    set -o allexport
    . /secretVol/secrets
else
    echo "No secrets file found"
fi

rc-service nginx start

uwsgi --ini uwsgi.ini