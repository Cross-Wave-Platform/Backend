#!/bin/bash

/opt/mssql/bin/sqlservr >/dev/null 2>&1 &
sleep 10

if [ -z ${PROJ_INIT+x} ]; then 
    python3 proj_setup/setup.py
    python3 -m test.test
else
    echo "already init"
fi

python3 app.py