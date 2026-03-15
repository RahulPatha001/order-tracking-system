from kafka import KafkaConsumer
from model.order_dto import order_dto
import os
import json
from dotenv import load_dotenv
load_dotenv()

KAFKA_BOOTSTRAP_SERVER = os.getenv('KAFKA_BOOTSTRAP_SERVERS')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC')
KAFKA_GROUP_ID = os.getenv('KAFKA_CONSUMER_GROUP_ID')

def order_consumer():

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVER,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id=KAFKA_GROUP_ID,
        value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    )

    print("Connected to Kafka:", consumer.bootstrap_connected())
    print("Listening to topic:", KAFKA_TOPIC)

    for message in consumer:
        print("Raw message:", message.value)

        try:
            order_obj = order_dto(**message.value)
            print("Parsed Order:", order_obj)
        except Exception as e:
            print("Error parsing message:", e)
        