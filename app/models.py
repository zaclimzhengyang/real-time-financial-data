from sqlalchemy import Table, Column, Integer, String, Float, DateTime, MetaData

metadata = MetaData()

stock_data = Table(
    "stock_data",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("ticker", String),
    Column("timestamp", DateTime),
    Column("open", Float),
    Column("high", Float),
    Column("low", Float),
    Column("close", Float),
    Column("prev_close", Float),
    Column("source", String),
)
