import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql+psycopg2://admin:secret123@localhost:5432/mydb"
)

new_customers = pd.DataFrame({
    "name": ["Nooshin", "Amir", "Fatemeh"],
    "email": [
        "nooshin@gmail.com",
        "amir@gmail.com",
        "fatemeh@gmail.com"
    ],
    "city": ["Tehran", "Karaj", "Qom"]
})

# Read existing emails from the database
existing_emails = pd.read_sql(
    "SELECT email FROM customers;",
    engine
)

# Keep only customers whose email does not already exist
new_customers = new_customers[
    ~new_customers["email"].isin(existing_emails["email"])
]

# Insert only if there is new data
if not new_customers.empty:
    new_customers.to_sql(
        "customers",
        engine,
        if_exists="append",
        index=False
    )
    print("Data inserted successfully!")
else:
    print("No new customers to insert.")