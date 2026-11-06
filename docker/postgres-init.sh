#!/bin/sh
set -eu

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" \
  --set=dev_db="$DEV_DB_NAME" \
  --set=dev_user="$DEV_DB_USER" \
  --set=dev_password="$DEV_DB_PASSWORD" \
  --set=staging_db="$STAGING_DB_NAME" \
  --set=staging_user="$STAGING_DB_USER" \
  --set=staging_password="$STAGING_DB_PASSWORD" <<'SQL'
CREATE ROLE :"dev_user" LOGIN PASSWORD :'dev_password';
CREATE DATABASE :"dev_db" OWNER :"dev_user";
CREATE ROLE :"staging_user" LOGIN PASSWORD :'staging_password';
CREATE DATABASE :"staging_db" OWNER :"staging_user";
SQL
