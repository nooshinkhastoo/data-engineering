from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.smtp.hooks.smtp import SmtpHook

from datetime import datetime
import os
import csv
import logging


logger = logging.getLogger(__name__)


BATCH_SIZE = 1000

CSV_FILE_PATH = "/opt/airflow/data/sales.csv"

EMAIL_TO = "nooshinkhastoo@gmail.com"

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_id",
    "product",
    "category",
    "quantity",
    "unit_price",
]


# ============================================================
# TASK 1
# Read and validate CSV
# ============================================================

def read_and_validate_csv():

    logger.info("Starting CSV file validation...")
    logger.info(f"CSV file path: {CSV_FILE_PATH}")
    logger.info(f"Batch size: {BATCH_SIZE}")

    # Check if file exists
    if not os.path.exists(CSV_FILE_PATH):

        logger.error(
            f"CSV file not found: {CSV_FILE_PATH}"
        )

        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE_PATH}"
        )

    logger.info("CSV file exists.")

    total_records = 0

    # Open CSV
    with open(
        CSV_FILE_PATH,
        "r",
        newline="",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        # Check header
        if reader.fieldnames is None:

            logger.error(
                "CSV file does not contain a header."
            )

            raise ValueError(
                "CSV file does not contain a header."
            )

        logger.info(
            f"CSV columns: {reader.fieldnames}"
        )

        # Check required columns
        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in reader.fieldnames
        ]

        if missing_columns:

            logger.error(
                f"Missing required columns: {missing_columns}"
            )

            raise ValueError(
                f"Missing required columns: {missing_columns}"
            )

        logger.info("CSV structure is valid.")

        # Process records in batches
        batch = []

        for row in reader:

            batch.append(row)

            if len(batch) == BATCH_SIZE:

                total_records += len(batch)

                logger.info(
                    f"Validated batch of {len(batch)} records. "
                    f"Total records processed: {total_records}"
                )

                batch = []

        # Process final batch
        if batch:

            total_records += len(batch)

            logger.info(
                f"Validated final batch of {len(batch)} records. "
                f"Total records processed: {total_records}"
            )

    logger.info(
        "CSV validation completed successfully. "
        f"Total records: {total_records}"
    )

    # This return value will automatically be stored in XCom
    return {
        "file_path": CSV_FILE_PATH,
        "total_records": total_records,
        "columns": REQUIRED_COLUMNS,
    }


# ============================================================
# TASK 2
# Load CSV into PostgreSQL
# ============================================================

def load_csv_to_postgres():

    logger.info("Starting PostgreSQL load...")

    # Use Airflow Connection
    hook = PostgresHook(
        postgres_conn_id="postgres_default"
    )

    connection = None
    cursor = None

    try:

        logger.info(
            "Connecting to PostgreSQL using Airflow Connection "
            "'postgres_default'..."
        )

        connection = hook.get_conn()

        cursor = connection.cursor()

        logger.info(
            "PostgreSQL connection established."
        )

        # Create sales table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sales (
            order_id INTEGER PRIMARY KEY,
            order_date DATE NOT NULL,
            customer_id INTEGER NOT NULL,
            product VARCHAR(255) NOT NULL,
            category VARCHAR(100) NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price NUMERIC(12, 2) NOT NULL
        );
        """

        cursor.execute(create_table_sql)

        logger.info(
            "Sales table is ready."
        )

        # Make the pipeline idempotent
        cursor.execute(
            "TRUNCATE TABLE sales;"
        )

        logger.info(
            "Sales table truncated before loading new data."
        )

        batch = []

        total_inserted = 0

        # Read CSV
        with open(
            CSV_FILE_PATH,
            "r",
            newline="",
            encoding="utf-8"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                batch.append(
                    (
                        int(row["order_id"]),
                        row["order_date"],
                        int(row["customer_id"]),
                        row["product"],
                        row["category"],
                        int(row["quantity"]),
                        float(row["unit_price"]),
                    )
                )

                # Insert batch
                if len(batch) == BATCH_SIZE:

                    insert_sql = """
                    INSERT INTO sales (
                        order_id,
                        order_date,
                        customer_id,
                        product,
                        category,
                        quantity,
                        unit_price
                    )
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                    """

                    cursor.executemany(
                        insert_sql,
                        batch
                    )

                    total_inserted += len(batch)

                    logger.info(
                        f"Inserted batch of {len(batch)} records. "
                        f"Total inserted: {total_inserted}"
                    )

                    batch = []

            # Insert final batch
            if batch:

                insert_sql = """
                INSERT INTO sales (
                    order_id,
                    order_date,
                    customer_id,
                    product,
                    category,
                    quantity,
                    unit_price
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                );
                """

                cursor.executemany(
                    insert_sql,
                    batch
                )

                total_inserted += len(batch)

                logger.info(
                    f"Inserted final batch of {len(batch)} records. "
                    f"Total inserted: {total_inserted}"
                )

        # Commit transaction
        connection.commit()

        logger.info(
            "PostgreSQL load completed successfully. "
            f"Total records inserted: {total_inserted}"
        )

    except Exception:

        # Rollback if anything fails
        if connection:

            connection.rollback()

        logger.exception(
            "PostgreSQL load failed. "
            "Transaction rolled back."
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        logger.info(
            "PostgreSQL connection closed."
        )


# ============================================================
# TASK 3
# Aggregate sales
# ============================================================

def aggregate_sales():

    logger.info(
        "Starting sales aggregation..."
    )

    hook = PostgresHook(
        postgres_conn_id="postgres_default"
    )

    connection = None
    cursor = None

    try:

        logger.info(
            "Connecting to PostgreSQL using Airflow Connection "
            "'postgres_default'..."
        )

        connection = hook.get_conn()

        cursor = connection.cursor()

        logger.info(
            "PostgreSQL connection established."
        )

        # Create aggregation table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS sales_aggregation (
            order_date DATE NOT NULL,
            category VARCHAR(100) NOT NULL,
            total_quantity INTEGER NOT NULL,
            total_sales NUMERIC(14, 2) NOT NULL,
            PRIMARY KEY (order_date, category)
        );
        """

        cursor.execute(
            create_table_sql
        )

        logger.info(
            "sales_aggregation table is ready."
        )

        # Make aggregation idempotent
        cursor.execute(
            "TRUNCATE TABLE sales_aggregation;"
        )

        logger.info(
            "sales_aggregation table truncated."
        )

        # Aggregate data
        aggregation_sql = """
        INSERT INTO sales_aggregation (
            order_date,
            category,
            total_quantity,
            total_sales
        )
        SELECT
            order_date,
            category,
            SUM(quantity) AS total_quantity,
            SUM(quantity * unit_price) AS total_sales
        FROM sales
        GROUP BY
            order_date,
            category;
        """

        cursor.execute(
            aggregation_sql
        )

        logger.info(
            "Sales aggregation completed."
        )

        # Count final aggregation records
        cursor.execute(
            "SELECT COUNT(*) FROM sales_aggregation;"
        )

        aggregation_count = cursor.fetchone()[0]

        logger.info(
            f"Final aggregation record count: "
            f"{aggregation_count}"
        )

        # Commit
        connection.commit()

        logger.info(
            "Sales aggregation transaction "
            "committed successfully."
        )

        # This value will automatically go to XCom
        return aggregation_count

    except Exception:

        if connection:

            connection.rollback()

        logger.exception(
            "Sales aggregation failed. "
            "Transaction rolled back."
        )

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()

        logger.info(
            "PostgreSQL connection closed."
        )


# ============================================================
# TASK 4
# Check aggregation result and send email if empty
# ============================================================

def check_aggregation_result(**context):

    logger.info(
        "Starting aggregation result check..."
    )

    # Get Task Instance
    ti = context["ti"]

    # Get result from Task 3 XCom
    aggregation_count = ti.xcom_pull(
        task_ids="aggregate_sales"
    )

    logger.info(
        f"Aggregation count received from XCom: "
        f"{aggregation_count}"
    )

    # Make sure XCom contains a value
    if aggregation_count is None:

        logger.error(
            "Aggregation count was not found in XCom."
        )

        raise ValueError(
            "Aggregation count was not found in XCom."
        )

    # If aggregation is empty
    if aggregation_count == 0:

        logger.warning(
            "Aggregation result contains 0 records."
        )

        subject = (
            "Airflow Warning - Empty Aggregation Result"
        )

        body = (
            "The sales aggregation pipeline completed successfully,\n"
            "but the final aggregation result contains 0 records.\n"
            "Please investigate the input data and pipeline execution."
        )

        logger.info(
            "Sending empty aggregation warning email..."
        )

        try:

            with SmtpHook(
                smtp_conn_id="smtp_default"
            ) as smtp_hook:

                smtp_hook.send_email_smtp(
                    to=EMAIL_TO,
                    from_email="airflow@example.com",
                    subject=subject,
                    html_content=body.replace(
                        "\n",
                        "<br>"
                    ),
                )

            logger.info(
                "Warning email sent successfully."
            )

        except Exception:

            logger.exception(
                "Failed to send warning email."
            )

            raise

    # If aggregation contains records
    else:

        logger.info(
            "Aggregation result contains records. "
            "No email notification is required."
        )

    logger.info(
        "Aggregation result check completed successfully."
    )


# ============================================================
# DAG
# ============================================================

with DAG(
    dag_id="sales_pipeline",
    start_date=datetime(2026, 9, 24),
    schedule=None,
    catchup=False,
) as dag:

    # Task 1
    read_csv_task = PythonOperator(
        task_id="read_and_validate_csv",
        python_callable=read_and_validate_csv,
    )

    # Task 2
    load_postgres_task = PythonOperator(
        task_id="load_csv_to_postgres",
        python_callable=load_csv_to_postgres,
    )

    # Task 3
    aggregate_task = PythonOperator(
        task_id="aggregate_sales",
        python_callable=aggregate_sales,
    )

    # Task 4
    check_result_task = PythonOperator(
        task_id="check_aggregation_result",
        python_callable=check_aggregation_result,
    )

    # Task dependencies
    (
        read_csv_task
        >> load_postgres_task
        >> aggregate_task
        >> check_result_task
    )