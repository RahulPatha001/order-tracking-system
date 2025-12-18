from Dto.order_dto import order_dto
from kafka import KafkaProducer
import json
import os

kafka_host = os.getenv("KAFKA_HOST")
kafka_port = os.getenv("KAFKA_PORT")
kafka_topic = os.getenv("KAFKA_TOPIC")

def send_to_status_service(order_details: order_dto):
    producer = KafkaProducer(bootstrap_servers=[f'{kafka_host}:{kafka_port}'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(kafka_topic, value=json.dumps(order_details))
    producer.flush()
    producer.close()
    