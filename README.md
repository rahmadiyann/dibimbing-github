# ETL Assignment DAG

## Overview

This Airflow DAG performs an Extract, Load, and Transform (ETL) process, moving data from MySQL to PostgreSQL for multiple tables related to a music streaming service. The DAG is designed to run every two hours from 9 AM to 9 PM on the 1st to 7th and 15th to 21st days of each month, but only in May (5th month).

## DAG Details

- **DAG File**: [assignment.py](airflow-docker/dags/assignment.py)
- **DAG ID**: `el_assignment`
- **Owner**: rian
- **Start Date**: October 5, 2024
- **Schedule**: `15 9-21/2 1-7,15-21 * 5` (At minute 15 past every 2nd hour from 9 through 21 on day-of-month 1 through 7 and 15 through 21 on the 5th day of the week/Friday)
- **Catchup**: False

## Tables Processed

The DAG processes the following tables (defined in `dags/resources/assignment/tables.yaml`):

1. dibimbing_songs
2. dibimbing_albums
3. dibimbing_artists
4. dibimbing_genres
5. dibimbing_playlists

## DAG Structure

1. **Start**: Empty operator to mark the beginning of the DAG.
2. **File System Precheck**: Creates a staging directory for temporary CSV files.
3. **MySQL Precheck**: Executes `mysql_precheck.sql` to set up and populate MySQL tables.
4. **PostgreSQL Precheck**: Executes `psql_precheck.sql` to create tables in PostgreSQL.
5. **Wait**: Empty operator to synchronize tasks.
6. **Extract Tasks**: For each table, extracts data from MySQL and saves to CSV.
7. **Load Tasks**: For each table, loads data from CSV to PostgreSQL.
8. **Cleanup**: Removes temporary CSV files.
9. **Show Data Tasks**: For each table, displays the data loaded into PostgreSQL.
10. **End**: Empty operator to mark the end of the DAG.

## Task Details

### File System Precheck
Creates a directory at [list tables.yaml](airflow-docker/dags/resources/assignment/tables.yaml) for storing temporary CSV files.

### MySQL Precheck
Executes [mysql_precheck.sql](airflow-docker/dags/resources/assignment/mysql_precheck.sql), which:
- Creates tables if they don't exist
- Truncates existing data
- Inserts sample data into each table

### PostgreSQL Precheck
Executes [psql_precheck.sql](airflow-docker/dags/resources/assignment/psql_precheck.sql), which: 
- Creates tables if they don't exist.
- Truncates existing data

### Extract Data
For each table:
- Connects to MySQL using `MySqlHook`
- Extracts all data from the table
- Saves the data to a CSV file in the staging directory

### Load Data
For each table:
- Reads the CSV file from the staging directory
- Connects to PostgreSQL using `PostgresHook`
- Loads the data into PostgreSQL, replacing existing data if the table already exists

### Show Data
For each table:
- Connects to PostgreSQL
- Retrieves all data from the table
- Prints the data to the console

## Dependencies

- Apache Airflow
- MySQL
- PostgreSQL
- pandas
- SQLAlchemy
- PyYAML

## Notes

- The DAG uses connection IDs `mysql_dibimbing` for MySQL and `postgres_dibimbing` for PostgreSQL.
- The staging directory is cleaned up after each run to prevent accumulation of temporary files.
- This DAG is designed for a specific use case and may need modifications for production environments or different data schemas.