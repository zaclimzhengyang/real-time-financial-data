# Real Time Financial Data Processing System using Kafka
![High Level Architecture Diagram.png](asset/High%20Level%20Architecture%20Diagram.png)

## Project Setup
### Install Dependencies
```
# Activate poetry virtual environment
poetry env activate

# Install project dependencies
poetry install

# Run Kafka and Zookeeper using Docker Compose
docker-compose up -d
```

## Register for free API key at Finnhub
Go to https://finnhub.io/register and sign up for a free account. After registering, you will receive an API key that you can use to access financial data.
Put the API key in a `.env` file in the root directory of the project as follows:
```
FINNHUB_API_KEY=your_api_key_here
```

## Run the Data Producer
Run both the producer and consumer in separate terminal windows.