import os
from dotenv import load_dotenv
from pathlib import Path
from kafka import KafkaProducer
from faker import Faker
from faker.providers import python
from time import sleep
from datetime import datetime, timedelta
import uuid
from sensor_data_pb2 import SensorData  # This will be generated from the proto file

dotenv_path = Path("/opt/app/.env")
# dotenv_path = Path("/Users/rian/Github/dibimbing-github/dibimbing_spark_airflow/kafka/assignment/.env")
load_dotenv(dotenv_path=dotenv_path)

kafka_host = os.getenv("KAFKA_HOST")
kafka_topic = os.getenv("KAFKA_TOPIC_NAME")
print(f"Kafka host: {kafka_host}")
print(f"Kafka topic: {kafka_topic}")

producer = KafkaProducer(bootstrap_servers=f"{kafka_host}:9092",
                        value_serializer=lambda x: x)
faker = Faker()


class DataGenerator(object):
    @staticmethod
    def get_data():
        now = datetime.now()
        sensor_data = SensorData()
        
        sensor_data.device_id = str(uuid.uuid4())
        sensor_data.sensor_type = faker.random_element(
            elements=("temperature_sensor", "humidity_sensor", "pressure_sensor", "air_quality_sensor")
        )
        sensor_data.device_version = faker.random_int(min=1, max=1000)
        sensor_data.location = faker.random_element(
            elements=("living_room", "bedroom", "kitchen", "bathroom", "garage")
        )
        sensor_data.temperature_celsius = faker.pyfloat(min_value=15, max_value=35, positive=True, right_digits=2, left_digits=2)
        sensor_data.humidity_percentage = faker.random_int(min=20, max=90)
        sensor_data.pressure_hpa = faker.random_int(min=980, max=1020)
        sensor_data.air_quality_index = faker.random_int(min=0, max=500)
        sensor_data.status = faker.random_element(elements=("normal", "warning", "critical"))
        sensor_data.is_active = faker.boolean()
        sensor_data.battery_level = faker.random_int(min=1, max=100)
        sensor_data.ts = faker.unix_time(
            start_datetime=now - timedelta(minutes=60), end_datetime=now
        )
        
        return sensor_data


while True:
    sensor_data = DataGenerator.get_data()
    serialized_data = sensor_data.SerializeToString()
    print("\n" + "="*50 + "\n")
    print(f"Message sent for device: {sensor_data.device_id}", flush=True)
    response = producer.send(topic=kafka_topic, value=serialized_data)
    # print(response.get())
    # print("=-" * 20, flush=True)
    sleep(3)
