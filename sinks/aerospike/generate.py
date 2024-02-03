from faker import Faker
import csv
import random
from tqdm import tqdm

fake = Faker()

# Generate customers data
customers = []
for i in tqdm(range(100000)):  # Generate 100 customers
    customer = [
        i,  # Assuming customer_id starts at 0
        fake.first_name(),
        fake.last_name(),
        fake.date_of_birth(minimum_age=18, maximum_age=90).isoformat(),
        fake.email(),
        fake.phone_number(),
        fake.address().replace('\n', ', '),  # Replace newlines in address
        fake.city(),
        fake.state(),
        fake.zipcode(),
        fake.country(),
    ]
    customers.append(customer)

print("customers completed")
# Write customers to CSV
with open('customers.csv', 'w',  encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['customer_id', 'first_name', 'last_name', 'dob', 'email', 'phone_number', 'address', 'city', 'state', 'zip_code', 'country'])
    writer.writerows(customers)

# Generate transactions data
transactions = []
for i in tqdm(range(5000000)):  # Generate 500 transactions
    transaction = [
        i,  # Assuming transaction_id starts at 0
        random.randint(0, len(customers)),  # Assuming customer IDs range from 0 to 99
        random.choice(['Deposit', 'Withdrawal', 'Transfer']),
        round(random.uniform(10.00, 10000.00), 2),
        'USD',
        fake.date_this_year().isoformat(),
        random.choice(['Completed', 'Pending', 'Cancelled']),
        fake.sentence(),
    ]
    transactions.append(transaction)

# Write transactions to CSV
with open('transactions.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_NONNUMERIC)
    writer.writerow(['transaction_id', 'customer_id', 'type', 'amount', 'currency', 'transaction_date', 'status', 'description'])
    writer.writerows(transactions)