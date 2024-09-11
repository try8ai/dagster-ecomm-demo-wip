import json
import csv
import random
from datetime import datetime, timedelta
import faker

# Initialize Faker
fake = faker.Faker()

# Constants
NUM_CUSTOMERS = 5341
NUM_PRODUCTS = 75
NUM_ORDER_LINES = 37421
NUM_ORDERS = 12210
NUM_VISITS = 510401

states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 
    'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 
    'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]
now = datetime.now()

# Helper Functions
def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def generate_customer_data():
    return [{
        "customer_id": i,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "city": fake.city(),
        "state": random.choice(states),
        "zipcode": fake.zipcode(),
    } for i in range(NUM_CUSTOMERS)]

def generate_products_data():
    categories = [
    'Electronics', 
    'Clothing', 
    'Books', 
    'Toys', 
    'Furniture', 
    'Home Appliances', 
    'Beauty', 
    'Health', 
    'Sports Equipment', 
    'Musical Instruments', 
    'Jewelry', 
    'Watches', 
    'Bags', 
    'Shoes', 
    'Accessories', 
    'Stationery', 
    'Office Supplies', 
    'Automotive', 
    'Outdoor', 
    'Garden Supplies'
    ]
    return [{
        "id": i,
        "name": 'Product ' + str(i),
        "category": random.choice(categories),
        "price_gross": random.uniform(10.0, 100.0),
        "price_net": lambda gross=random.uniform(10.0, 100.0): round(gross * 0.9, 2),  # Assuming tax rate is 10%
    } for i in range(NUM_PRODUCTS)]

def generate_orders_data(customers):
    orders = []
    for i in range(NUM_ORDERS):
        customer = random.choice(customers)
        total_gross = random.uniform(20.0, 200.0)
        total_tax = round(total_gross * 0.1, 2)  # 10% tax
        orders.append({
            "order_id": i,
            "created_at": random_date(now - timedelta(days=365), now).strftime('%Y-%m-%d %H:%M:%S'),
            "currency_code": "USD",
            "receipt_number": 'RCPT' + str(i).zfill(6),
            "total_gross": total_gross,
            "total_tax": total_tax,
            "total_net": round(total_gross - total_tax, 2),
            "payment_method": random.choice(['Credit Card', 'Paypal', 'Bitcoin']),
            "paid_amount": total_gross,
            "customer_id": customer["customer_id"],
        })
    return orders

def generate_order_lines_data(orders, products):
    order_lines = []
    for i in range(NUM_ORDER_LINES):
        order = random.choice(orders)
        product = random.choice(products)
        quantity = random.randint(1, 5)
        unit_price = product["price_gross"]
        total_price = round(unit_price * quantity, 2)
        order_lines.append({
            "order_lines_id": i,
            "unit_price": unit_price,
            "price_net": product["price_net"](),
            "tax_rate": 0.1,
            "tax_amount": round(unit_price * 0.1, 2),
            "total_price": total_price,
            "quantity": quantity,
            "created_at": order["created_at"],
            "product_id": product["id"],
            "order_id": order["order_id"],
            "category": product["category"],
        })
    return order_lines

def generate_analytics_event(customer_state_map, customer_id):
    event_date = random_date(now - timedelta(days=365), now)
    pseudo_id = fake.uuid4()

    event = {
        "event_date": event_date.strftime('%Y-%m-%d'),
        "event_timestamp": int(event_date.timestamp() * 1000000),
        "event_name": random.choice(['page_view', 'purchase', 'sign_up', 'add_to_cart']),
        "event_params": [
            {
                "key": "page_path",
                "value": {
                    "string_value": '/product/' + str(random.randint(1, 100)),
                }
            },
        ],
        "user_id": customer_id,
        "user_pseudo_id": pseudo_id,
        "geo": {
            "continent": 'North America',
            "country": 'United States',
            "region": customer_state_map[customer_id],
            "city": fake.city()
        },
        "traffic_source": {
            "name": fake.random_element(elements=['google', 'facebook', 'organic']),
            "medium": fake.random_element(elements=['cpc', 'social', 'organic']),
            "source": fake.random_element(elements=['google', 'facebook', 'bing', 'yahoo'])
        }
    }

    return event

def customer_state_mapping(customers):
    customer_state_map = {}
    for customer in customers:
        customer_state_map[customer["customer_id"]] = customer["state"]
    return customer_state_map

def generate_analytics_events(customer_state_map, customer_ids):
    events = []
    for customer_id in customer_ids:
        num_events = random.randint(1, 5)  # Create multiple events per customer
        for _ in range(num_events):
            events.append(generate_analytics_event(customer_state_map, customer_id))
    return events

# Writing data to CSV
def write_csv(filename, fieldnames, rows):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: (v() if callable(v) else v) for k, v in row.items()})

customers = generate_customer_data()
products = generate_products_data()
orders = generate_orders_data(customers)
order_lines = generate_order_lines_data(orders, products)

write_csv('customers.csv', customers[0].keys(), customers)
write_csv('products.csv', products[0].keys(), products)
write_csv('orders.csv', orders[0].keys(), orders)
write_csv('order_lines.csv', order_lines[0].keys(), order_lines)

# Generate correlated Google Analytics data
customer_ids = [customer["customer_id"] for customer in customers]
customer_state_map = customer_state_mapping(customers)
analytics_data = {
    "analytics_website": {
        "tables": {
            f"events_{now.strftime('%Y%m%d')}": generate_analytics_events(customer_state_map, customer_ids)
        }
    }
}

# Write to JSON file
with open('google_analytics.json', 'w') as jsonfile:
    json.dump(analytics_data, jsonfile, indent=4)
