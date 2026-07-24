FROM postgres:17

COPY init.sql /docker-entrypoint-initdb.d/01-init.sql
COPY setup-hba.sh /docker-entrypoint-initdb.d/02-setup-hba.sh