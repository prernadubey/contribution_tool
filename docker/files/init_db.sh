#!/usr/bin/env bash

db_exist_check=$(PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME}  -lqt | cut -d \| -f 1 | grep -qw ${DB_NAME})

db_empty_check=$(PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME} -d ${DB_NAME}  -At <<EOF
select count(*) from pg_class c join pg_namespace s on s.oid = c.relnamespace where s.nspname not in ('pg_catalog', 'information_schema') and c.relname = 'alembic_version';
EOF
)

if $db_exist_check; then
  echo "[init-db] Database exists."
else
  PGPASSWORD=${DB_PASSWORD} psql -h ${DB_HOST} -p ${DB_PORT} -U ${DB_USERNAME} -d postgres -c \
  "CREATE DATABASE ${DB_NAME};"
fi

if [ $db_empty_check != 0 ]; then
  echo "[init-db] Database is not empty."
else
  alembic upgrade head
fi

