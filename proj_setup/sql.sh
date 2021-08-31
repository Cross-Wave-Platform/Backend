#!/bin/bash

for i in {1..50};
do
    /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Kit2021db -d master -i ./proj_setup/DDL.sql
    if [ $? -eq 0 ]
    then
        echo "setup.sql completed"
        break
    else
        echo "not ready yet..."
        sleep 1
    fi
done