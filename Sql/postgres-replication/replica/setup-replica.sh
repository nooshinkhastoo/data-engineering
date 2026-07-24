#!/bin/bash
set -e

echo "Waiting for master..."

until pg_isready -h pg-master -U admin; do
    sleep 2
done

echo "Master is ready"

if [ ! -s "$PGDATA/PG_VERSION" ]; then

    echo "Initializing replica..."

    rm -rf "$PGDATA"/*

    PGPASSWORD=replica123 pg_basebackup \
        -h pg-master \
        -D "$PGDATA" \
        -U replicator \
        -Fp \
        -Xs \
        -P \
        -R

    echo "Replica initialized"

else

    echo "Replica already initialized"

fi


echo "Starting PostgreSQL..."

exec docker-entrypoint.sh postgres