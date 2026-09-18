from cassandra.cluster import Cluster

cluster = Cluster([
    "cassandra1",
    "cassandra2",
    "cassandra3"
])
session = cluster.connect()

print("Connected to Cassandra!")


# Create keyspace
session.execute("""
    CREATE KEYSPACE IF NOT EXISTS shop
    WITH replication = {
        'class': 'SimpleStrategy',
        'replication_factor': 1
    }
""")

print("Keyspace created!")


# Create users table
session.execute("""
    CREATE TABLE IF NOT EXISTS shop.users (
        id int PRIMARY KEY,
        name text,
        email text,
        age int
    )
""")

print("Table created!")


# Insert first user
session.execute("""
    INSERT INTO shop.users (id, name, email, age)
    VALUES (1, 'Nooshin', 'nooshin@example.com', 30)
""")

print("User inserted!")


# Select all users
rows = session.execute("""
    SELECT id, name, email, age
    FROM shop.users
""")

for row in rows:
    print(
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}, "
        f"age={row.age}"
    )


# Update user
session.execute("""
    UPDATE shop.users
    SET age = 31
    WHERE id = 1
""")

print("User updated!")


# Select updated user
rows = session.execute("""
    SELECT id, name, email, age
    FROM shop.users
    WHERE id = 1
""")

for row in rows:
    print(
        f"After update: "
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}, "
        f"age={row.age}"
    )


# Insert more users
session.execute("""
    INSERT INTO shop.users (id, name, email, age)
    VALUES (2, 'Sara', 'sara@example.com', 25)
""")

session.execute("""
    INSERT INTO shop.users (id, name, email, age)
    VALUES (3, 'Ali', 'ali@example.com', 28)
""")

print("More users inserted!")


# Select all users
rows = session.execute("""
    SELECT id, name, email, age
    FROM shop.users
""")

print("All users:")

for row in rows:
    print(
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}, "
        f"age={row.age}"
    )


# Select user by partition key
rows = session.execute("""
    SELECT id, name, email, age
    FROM shop.users
    WHERE id = 2
""")

print("User with id=2:")

for row in rows:
    print(
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}, "
        f"age={row.age}"
    )


# Search by age using ALLOW FILTERING
rows = session.execute("""
    SELECT id, name, email, age
    FROM shop.users
    WHERE age = 25
    ALLOW FILTERING
""")

print("Users with age=25:")

for row in rows:
    print(
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}, "
        f"age={row.age}"
    )


# Create query-based table
session.execute("""
    CREATE TABLE IF NOT EXISTS shop.users_by_age (
        age int,
        id int,
        name text,
        email text,
        PRIMARY KEY (age, id)
    )
""")

print("users_by_age table created!")


# Insert users into users_by_age
session.execute("""
    INSERT INTO shop.users_by_age (age, id, name, email)
    VALUES (25, 2, 'Sara', 'sara@example.com')
""")

session.execute("""
    INSERT INTO shop.users_by_age (age, id, name, email)
    VALUES (25, 4, 'Mary', 'mary@example.com')
""")

session.execute("""
    INSERT INTO shop.users_by_age (age, id, name, email)
    VALUES (28, 3, 'Ali', 'ali@example.com')
""")

print("Users inserted into users_by_age!")
rows = session.execute("""
    SELECT age, id, name, email
    FROM shop.users_by_age
    WHERE age = 25
""")

print("Users with age=25 from users_by_age:")

for row in rows:
    print(
        f"age={row.age}, "
        f"id={row.id}, "
        f"name={row.name}, "
        f"email={row.email}"
    )