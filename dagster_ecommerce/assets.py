from dagster import asset
from dagster_duckdb import DuckDBResource

@asset
def products(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE products AS SELECT * FROM read_parquet('data/shopping/products.parquet')")

@asset
def customers(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE customers AS SELECT * FROM read_parquet('data/shopping/customers.parquet')")

@asset
def orders(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE orders AS SELECT * FROM read_parquet('data/shopping/orders.parquet')")

@asset
def order_lines(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE order_lines AS SELECT * FROM read_parquet('data/shopping/order_lines.parquet')")
