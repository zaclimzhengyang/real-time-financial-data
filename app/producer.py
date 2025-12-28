import json
import time
import requests
from kafka import KafkaProducer
from config.settings import (
    KAFKA_BOOTSTRAP_SERVERS,
    KAFKA_TOPIC)

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    linger_ms=50
)

def fetch_and_send(tickers: list):
    for ticker in tickers:
        try:
            resp = requests.get(
                "https://finnhub.io/api/v1/quote",
                params={
                    "symbol": ticker,
                    "token": ""
                },
                timeout=5
            )

            if resp.status_code != 200:
                print(f"🔴 HTTP error {resp.status_code} for {ticker}")
                continue

            data = resp.json()

            # Finnhub returns 0s when market closed
            if data.get("t", 0) == 0:
                print(f"🟡 No market data for {ticker}")
                continue

            record = {
                "ticker": ticker,
                "timestamp": data["t"],   # unix epoch
                "open": data["o"],
                "high": data["h"],
                "low": data["l"],
                "close": data["c"],
                "prev_close": data["pc"],
                "source": "finnhub"
            }

            producer.send(KAFKA_TOPIC, record)
            print(f"🟢 Sent {ticker} @ {data['c']}")

        except Exception as e:
            print(f"🔴 Error fetching {ticker}: {e}")

    producer.flush()


if __name__ == "__main__":
    STOCKS = ["AAPL", "MSFT", "GOOGL"] # example

    while True:
        fetch_and_send(STOCKS)
        time.sleep(60)
