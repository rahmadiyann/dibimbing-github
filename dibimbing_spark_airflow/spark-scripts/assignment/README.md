# Kafka Sensor Data Streaming Assignment

This project demonstrates a real-time sensor data streaming application using Apache Kafka with Protocol Buffers (protobuf) for efficient data serialization. The system simulates IoT sensors sending environmental data and processes it in real-time.

## Architecture Overview

The project consists of:

- A Kafka producer that generates simulated sensor data
- A Kafka consumer that processes and displays metrics in real-time
- Protocol Buffers for data serialization
- A Kafka cluster with UI management tools

## Prerequisites

- Docker and Docker Compose
- Python 3.8+
- Protocol Buffers compiler (protoc)

## Required Python Packages

```bash
pip install kafka-python python-dotenv faker protobuf
```

## Project Structure

```kafka/assignment/
├── producer.py           # Generates and sends sensor data
├── consumer.py          # Processes and displays metrics
├── sensor_data.proto    # Protocol Buffers definition
├── sensor_data_pb2.py   # Generated Protocol Buffers code
└── .env                 # Environment variables
```

## Protocol Buffer Schema

The sensor data schema is defined in `sensor_data.proto`:

- device_id (string)
- sensor_type (string)
- device_version (int32)
- location (string)
- temperature_celsius (float)
- humidity_percentage (int32)
- pressure_hpa (int32)
- air_quality_index (int32)
- status (string)
- is_active (bool)
- battery_level (int32)
- timestamp (int64)

## Infrastructure Setup

The infrastructure is defined in `docker-compose-kafka.yml` and includes:

- Kafka broker
- ksqlDB server
- Kafka UI interface

### Starting the Infrastructure

```bash
docker-compose -f docker/docker-compose-kafka.yml up -d
```

Access Kafka UI at: http://localhost:8083

## Running the Application

1. Start the consumer:

```bash
python kafka/assignment/consumer.py
```

2. In a separate terminal, start the producer:

```bash
python kafka/assignment/producer.py
```

## Features

### Producer

- Generates realistic sensor data using Faker
- Simulates different sensor types and locations
- Uses Protocol Buffers for efficient serialization
- Sends data every 3 seconds

### Consumer

- Processes messages in real-time
- Calculates running averages for:
  - Temperature
  - Humidity
  - Pressure
  - Air Quality
- Tracks critical alerts and low battery warnings
- Displays formatted metrics output

## Metrics Tracked

The consumer tracks and displays:

- Average temperature (°C)
- Average humidity (%)
- Average pressure (hPa)
- Average air quality index
- Total critical alerts
- Total low battery alerts

## Environment Variables

Required environment variables in `.env`:

- KAFKA_HOST: Kafka broker hostname
- KAFKA_TOPIC_NAME: Topic for sensor data
- KAFKA_CONTAINER_NAME: Docker container name for Kafka
- KSQL_CONTAINER_NAME: Docker container name for ksqlDB
- KSQL_HOST: ksqlDB hostname

## Error Handling

The application includes:

- Graceful shutdown on keyboard interrupt
- Auto-commit of consumer offsets
- Error handling for message serialization/deserialization

## Performance Considerations

- Uses Protocol Buffers for efficient serialization
- Implements consumer group for scalable message processing
- Configurable message production interval
