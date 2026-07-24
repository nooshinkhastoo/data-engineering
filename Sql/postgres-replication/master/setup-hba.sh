#!/bin/bash
set -e

echo "Configuring pg_hba.conf..."

cat >> "$PGDATA/pg_hba.conf" <<EOF

host    replication     replicator     all     scram-sha-256

EOF

echo "pg_hba.conf updated"