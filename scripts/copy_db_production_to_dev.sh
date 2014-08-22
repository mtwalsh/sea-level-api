#!/bin/bash -ex

function get_latest_database_dump {
    DUMP_FILE=heroku_production_database.dump

    if [ ! -f ${DUMP_FILE} ]; then
        BACKUP_URL=$(heroku pgbackups:url -a DATABASE_URL --app sea-level-api)
        curl -o ${DUMP_FILE} ${BACKUP_URL}
    fi
}

function convert_to_sql_file {
SQL_FILE=$(mktemp --suffix .sql)
    pg_restore --no-acl --no-owner -f ${SQL_FILE} ${DUMP_FILE}
}

function load_sql_file_to_database {
    dropdb ${USER}
    createdb ${USER}
    TEMP_LOG=$(mktemp --suffix .log)
    psql < ${SQL_FILE} > ${TEMP_LOG}
    less ${TEMP_LOG}
}

get_latest_database_dump
convert_to_sql_file
load_sql_file_to_database
