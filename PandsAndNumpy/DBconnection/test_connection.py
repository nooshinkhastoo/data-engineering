import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:secret123@localhost:5432/mydb"
)

# -------------------------------
# Query 1: PostgreSQL Version
# -------------------------------
version_query = "SELECT version();"

df_version = pd.read_sql(version_query, engine)

print(f"\n{'=' * 20} PostgreSQL Version {'=' * 20}")
print(df_version)


# -------------------------------
# Query 2: List Tables
# -------------------------------
tables_query = """
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';
"""

df_tables = pd.read_sql(tables_query, engine)

print(f"\n{'=' * 20} Tables {'=' * 20}")
print(df_tables)


# -------------------------------
# Query 3: Read customers table
# -------------------------------
customers_query = """
SELECT *
FROM customers
LIMIT 5;
"""

df_customers = pd.read_sql(customers_query, engine)

print(f"\n{'=' * 20} Customers {'=' * 20}")
print(df_customers)

print(f"\nShape: {df_customers.shape}")
print(f"\nData Types:\n{df_customers.dtypes}")


# ==========================================================
# Method 1 : read_sql()
# ==========================================================

print(f"\n{'=' * 20} Method 1 : read_sql() {'=' * 20}")

df_read_sql = pd.read_sql(
    "SELECT * FROM customers LIMIT 3;",
    engine
)

print(df_read_sql)


# ==========================================================
# Method 2 : read_sql_query()
# ==========================================================

print(f"\n{'=' * 20} Method 2 : read_sql_query() {'=' * 20}")

df_read_sql_query = pd.read_sql_query(
    "SELECT * FROM customers LIMIT 3;",
    engine
)

print(df_read_sql_query)


# ==========================================================
# Method 3 : read_sql_table()
# ==========================================================

print(f"\n{'=' * 20} Method 3 : read_sql_table() {'=' * 20}")

df_read_sql_table = pd.read_sql_table(
    "customers",
    engine
)

print(df_read_sql_table.head(3))



schema_query = """
SELECT
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'customers';
"""

df_schema = pd.read_sql(schema_query, engine)

print(df_schema)



print(f"\n{'=' * 20} Last Customers {'=' * 20}")

df_last_customers = pd.read_sql(
    """
    SELECT *
    FROM customers
    ORDER BY id DESC
    LIMIT 5;
    """,
    engine
)

print(df_last_customers)