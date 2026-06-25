import numpy as np

data = [
    ("Alice", 34, 70000),
    ("Bob", 45, 85000),
    ("Charlie", 25, 50000),
    ("Diana", 40, 90000),
    ("Eve", 29, 62000)
]

# 1.
employees = np.array(
    data,
    dtype=[
        ('name', 'U20'),
        ('age', 'i4'),
        ('salary', 'i4')
    ]
)

print(f"Employees:{employees}")

# 2. 
avg_salary_over_30 = np.mean(employees['salary'][employees['age'] > 30])

print(f"Average salary of employees older than 30: {avg_salary_over_30}")

# 3.
overall_avg_salary = np.mean(employees['salary'])

high_salary_names = employees['name'][employees['salary'] > overall_avg_salary]

print(f"Employees with salary above average: {high_salary_names}")

# 4.
sorted_employees = np.sort( employees, order='salary')[::-1]

print(f"Employees sorted by salary (descending):{sorted_employees}")