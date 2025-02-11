#!/bin/bash

echo "Setting up database."
sqlite3 ./database/CI.db < ./database/database_tables.sql
