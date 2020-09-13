#!/bin/bash
set -e

psql -U postgres <<-EOSQL
    CREATE USER scrapnow WITH password 'scrapnow';
EOSQL

createdb --encoding=utf-8 --owner=scrapnow -U postgres scrapnow


cat /latest.sql | psql -U scrapnow scrapnow


cp /postgresql.conf /var/lib/postgresql/data/postgresql.conf
