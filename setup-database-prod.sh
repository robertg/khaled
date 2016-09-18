#!/bin/sh

set -ex

sudo docker exec -it roach1 bash -c "
./cockroach sql -e 'DROP DATABASE IF EXISTS khaled;'
./cockroach sql -e 'CREATE DATABASE khaled;'
./cockroach sql -e 'drop table if exists khaled.entries;'
./cockroach sql -e 'GRANT ALL ON DATABASE khaled TO sixgod;'"

python -c 'import khaled; khaled.db.create_all()'
