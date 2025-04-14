#!/bin/bash

# Extract the current path that the user is in
path="${PWD##*/}"

# Create the database using the schema
if [ $path != "database" ]; then
    cat database/schema.sql | sqlite3 database.db
    mv database.db database/
else
    cat schema.sql | sqlite3 database.db
fi