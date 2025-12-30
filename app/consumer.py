import json
import datetime
from kafka import KafkaConsumer
from sqlalchemy import Engine, insert
from app.models import stock_data
from config.settings import KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC

consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="stock-consumers",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)


def save_to_db(record: dict, engine: Engine):
    stmt = insert(stock_data).values(
        ticker=record["ticker"],
        timestamp=datetime.datetime.fromtimestamp(record["timestamp"], tz=datetime.timezone.utc),
        open=record["open"],
        high=record["high"],
        low=record["low"],
        close=record["close"],
        prev_close=record["prev_close"],
        source=record["source"]
    )

    with engine.connect() as conn:
        try:
            conn.execute(stmt)
            conn.commit()
            print(f"💾 Saved {record['ticker']} @ {record['timestamp']}")
        except Exception as e:
            print(f"🔴 DB error: {e}")


if __name__ == "__main__":
    for msg in consumer:
        # save_to_db(msg.value)
        print(f"📥 Received: {msg.value}")
