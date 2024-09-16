import json
import requests

import pandas as pd

from dagster import (
    Config,
    MaterializeResult,
    MetadataValue,
    asset,
)

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


class HNStoriesConfig(Config):
    top_stories_limit: int = 10
    hn_top_story_ids_path: str = "hackernews_top_story_ids.json"
    hn_top_stories_path: str = "hackernews_top_stories.csv"


@asset
def hackernews_top_story_ids(config: HNStoriesConfig):
    """Get top stories from the HackerNews top stories endpoint."""
    top_story_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()

    with open(config.hn_top_story_ids_path, "w") as f:
        json.dump(top_story_ids[: config.top_stories_limit], f)


@asset(deps=[hackernews_top_story_ids])
def hackernews_top_stories(config: HNStoriesConfig) -> MaterializeResult:
    """Get items based on story ids from the HackerNews items endpoint."""
    with open(config.hn_top_story_ids_path, "r") as f:
        hackernews_top_story_ids = json.load(f)

    results = []
    for item_id in hackernews_top_story_ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json").json()
        results.append(item)

    df = pd.DataFrame(results)
    df.to_csv(config.hn_top_stories_path)

    return MaterializeResult(
        metadata={
            "num_records": len(df),
            "preview": MetadataValue.md(str(df[["title", "by", "url"]].to_markdown())),
        }
    )
