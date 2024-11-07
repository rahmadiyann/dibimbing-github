import os
from dotenv import load_dotenv
from pathlib import Path
from kafka import KafkaConsumer
from datetime import datetime
from sensor_data_pb2 import SensorData  # This will be generated from the proto file

dotenv_path = Path("/opt/app/.env")
# dotenv_path = Path("/Users/rian/Github/dibimbing-github/dibimbing_spark_airflow/kafka/assignment/.env")
load_dotenv(dotenv_path=dotenv_path)

kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC_NAME")
print(f"Kafka host: {kafka_host}")
print(f"Kafka topic: {kafka_topic}")

# Initialize Kafka consumer
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=f"{kafka_host}:9092",
    auto_offset_reset='earliest',
    # enable_auto_commit=True,
    # group_id='sensor_data_group',
    value_deserializer=lambda x: SensorData().FromString(x)
)

# Initialize metrics storage
metrics = {
    'temperature': {'sum': 0, 'count': 0},
    'humidity': {'sum': 0, 'count': 0},
    'pressure': {'sum': 0, 'count': 0},
    'air_quality': {'sum': 0, 'count': 0},
    'critical_alerts': 0,
    'low_battery_alerts': 0
}

print("Starting to consume messages...", flush=True)

try:
    for message in consumer:
        data = message.value  # This is now a SensorData object
        
        # Process temperature data
        metrics['temperature']['sum'] += data.temperature_celsius
        metrics['temperature']['count'] += 1
        avg_temp = metrics['temperature']['sum'] / metrics['temperature']['count']
        
        # Process humidity data
        metrics['humidity']['sum'] += data.humidity_percentage
        metrics['humidity']['count'] += 1
        avg_humidity = metrics['humidity']['sum'] / metrics['humidity']['count']
        
        # Process pressure data
        metrics['pressure']['sum'] += data.pressure_hpa
        metrics['pressure']['count'] += 1
        avg_pressure = metrics['pressure']['sum'] / metrics['pressure']['count']
        
        # Process air quality data
        metrics['air_quality']['sum'] += data.air_quality_index
        metrics['air_quality']['count'] += 1
        avg_air_quality = metrics['air_quality']['sum'] / metrics['air_quality']['count']
        
        # Track critical alerts
        if data.status == 'critical':
            metrics['critical_alerts'] += 1
            
        # Track low battery alerts (below 20%)
        if data.battery_level < 20:
            metrics['low_battery_alerts'] += 1
            
        # Print current metrics
        print("\n" + "="*50)
        print(f"Message received from {data.location} - {data.sensor_type}")
        print(f"Timestamp: {datetime.fromtimestamp(data.ts)}")
        print("\nCurrent Averages:")
        print(f"Temperature: {avg_temp:.2f}°C")
        print(f"Humidity: {avg_humidity:.2f}%")
        print(f"Pressure: {avg_pressure:.2f} hPa")
        print(f"Air Quality Index: {avg_air_quality:.2f}")
        print(f"\nTotal Critical Alerts: {metrics['critical_alerts']}")
        print(f"Total Low Battery Alerts: {metrics['low_battery_alerts']}")
        print("="*50 + "\n", flush=True)

except KeyboardInterrupt:
    print("\nStopping the consumer...")
    consumer.close()
