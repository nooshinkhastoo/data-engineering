# Airflow Sales Pipeline

A simple ETL pipeline built with Apache Airflow, PostgreSQL, and Mailpit.

The pipeline reads sales data from a CSV file, validates the input, loads the data into PostgreSQL, creates an aggregated sales table, and sends an email notification when the final aggregation contains zero records.

## Project Overview

The pipeline consists of four sequential tasks:

```text
Read and Validate CSV
        |
        v
Load Data into PostgreSQL
        |
        v
Aggregate Sales
        |
        v
Check Aggregation Result
        |
        +----> Send Email if result is empty
```

## Project Structure

```text
airflow-sales-pipeline/
├── dags/
│   └── sales_pipeline.py
├── data/
│   └── sales.csv
├── logs/
├── plugins/
├── config/
├── docker-compose.yaml
├── requirements.txt
└── README.md
```

## Technologies

* Apache Airflow 3.0.6
* Python
* PostgreSQL
* Docker
* Mailpit
* CSV
* Airflow Connections
* Airflow XCom
* PythonOperator
* PostgresHook
* SmtpHook

## Pipeline Tasks

### Task 1: Read and Validate CSV

Task ID:

```text
read_and_validate_csv
```

This task:

* Checks whether the CSV file exists.
* Reads the CSV file.
* Checks that the file contains a header.
* Validates the required columns.
* Processes records in batches.
* Logs the number of records.
* Fails the task if the file does not exist.
* Fails the task if required columns are missing.

Required columns:

```text
order_id
order_date
customer_id
product
category
quantity
unit_price
```

The CSV file used by the project is:

```text
data/sales.csv
```

### Task 2: Load CSV into PostgreSQL

Task ID:

```text
load_csv_to_postgres
```

This task loads the CSV records into the PostgreSQL table:

```text
sales
```

The table contains:

```text
order_id
order_date
customer_id
product
category
quantity
unit_price
```

The task uses the Airflow PostgreSQL Connection:

```text
postgres_default
```

Database credentials are not hard-coded in the DAG.

The task uses a database transaction:

1. Create the table if it does not exist.
2. Truncate the existing data.
3. Insert the CSV records.
4. Commit the transaction if everything succeeds.
5. Roll back the transaction if an error occurs.

This prevents a failed load from leaving partial data in the database.

### Task 3: Aggregate Sales

Task ID:

```text
aggregate_sales
```

This task creates the table:

```text
sales_aggregation
```

Sales are grouped by:

```text
order_date
category
```

The following values are calculated:

```text
total_quantity
total_sales
```

The final number of aggregation records is returned by the task.

The returned value is automatically stored in Airflow XCom.

### Task 4: Check Aggregation Result

Task ID:

```text
check_aggregation_result
```

This task gets the aggregation count from XCom.

It does not query PostgreSQL to calculate the count again.

If the aggregation count is greater than zero, no email is sent.

If the aggregation count is zero, an email notification is sent.

Email subject:

```text
Airflow Warning - Empty Aggregation Result
```

Email body:

```text
The sales aggregation pipeline completed successfully,
but the final aggregation result contains 0 records.
Please investigate the input data and pipeline execution.
```

## Airflow Connections

### PostgreSQL

The DAG uses:

```text
Connection ID: postgres_default
Connection Type: PostgreSQL
Host: postgres
Port: 5432
Database: airflow
```

The PostgreSQL connection is accessed through `PostgresHook`.

### SMTP

Mailpit is used as a local SMTP server for testing email notifications.

The Airflow SMTP Connection is:

```text
Connection ID: smtp_default
Connection Type: SMTP
Host: mailpit
Port: 1025
```

SSL/TLS is disabled because Mailpit is running as a local plain SMTP server.

Mailpit web interface:

```text
http://localhost:8025
```

## XCom

Task 3 returns the final aggregation count:

```python
return aggregation_count
```

Airflow automatically stores this value in XCom.

Task 4 retrieves the value using:

```python
ti.xcom_pull(
    task_ids="aggregate_sales"
)
```

Only the aggregation count is passed through XCom.

The full CSV data is not passed through XCom.

## Error Handling

The pipeline includes error handling for file, database, and email failures.

### Missing CSV File

If the CSV file does not exist, Task 1 raises a `FileNotFoundError`.

The task fails and downstream tasks are not executed.

Example log:

```text
CSV file not found: /opt/airflow/data/sales.csv
```

### Missing Required Columns

If one or more required columns are missing, Task 1 raises a `ValueError`.

### PostgreSQL Errors

Database errors are caught and logged.

If an error occurs during the loading transaction:

```text
PostgreSQL load failed. Transaction rolled back.
```

The transaction is rolled back and the error is raised again so that the Airflow task is marked as failed.

### Email Errors

If the warning email cannot be sent, the error is logged and the Airflow task fails.

## Idempotency

The pipeline is designed to be safely rerun.

Before loading new data, the `sales` table is truncated:

```sql
TRUNCATE TABLE sales;
```

The `sales_aggregation` table is also truncated before creating a new aggregation result.

Therefore, rerunning the DAG does not continuously add duplicate records from previous successful runs.

## Test Results

The pipeline was tested with several scenarios.

### Normal Run

The sample CSV contains 5 sales records.

All four tasks completed successfully.

The aggregation result contains 4 records.

```text
Task 1: Success
Task 2: Success
Task 3: Success
Task 4: Success
```

### Empty Aggregation

A header-only CSV file was used as input.

The pipeline successfully completed the first three tasks and Task 3 returned:

```text
0
```

Task 4 retrieved the value from XCom and sent the warning email.

The email was successfully received in Mailpit.

### Missing File

The CSV file was temporarily removed.

Task 1 failed with:

```text
FileNotFoundError
```

The downstream tasks were not executed.

### PostgreSQL Constraint Error

A test CSV containing a duplicate `order_id` was used.

PostgreSQL returned a primary key violation:

```text
duplicate key value violates unique constraint "sales_pkey"
```

The transaction was rolled back.

The original data remained in the `sales` table, confirming that the failed load did not leave partial data.

### Idempotency Test

The successful DAG was executed multiple times.

The final number of records in the `sales` table remained:

```text
5
```

No duplicate records were created by repeated successful runs.

## Running the Project

### First-Time Initialization

Initialize the Airflow database:

```bash
docker compose up airflow-init
```

### Start the Services

```bash
docker compose up -d
```

### Check Services

```bash
docker compose ps
```

### Airflow Web Interface

Open:

```text
http://localhost:8080
```

### Mailpit Web Interface

Open:

```text
http://localhost:8025
```

### DAG

The DAG ID is:

```text
sales_pipeline
```

The DAG can be triggered from the Airflow web interface.

## Requirements

The project uses the following Airflow providers:

```text
apache-airflow-providers-postgres
apache-airflow-providers-smtp
```

These are listed in:

```text
requirements.txt
```

## Stopping the Project

To stop the containers while keeping the Docker volumes:

```bash
docker compose stop
```

To start them again:

```bash
docker compose start
```

## Notes

The project uses Docker Compose to run Airflow, PostgreSQL, Redis, and Mailpit.

Airflow Connections are used for PostgreSQL and SMTP access instead of hard-coding database or SMTP connection details inside the DAG.
