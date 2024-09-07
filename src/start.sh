#!/usr/bin/env bash

if [ -f "/secretVol/secrets" ]; then
    echo "Loading secrets from /secretVol/secrets"
    set -o allexport
    . /secretVol/secrets
else
    echo "No secrets file found"
fi

service nginx start

uwsgi --ini uwsgi.ini
