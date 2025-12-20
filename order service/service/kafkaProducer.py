from Dto.order_dto import order_dto
from kafka import KafkaProducer
import json
import os
from dotenv import load_dotenv
load_dotenv()

kafka_host = os.getenv("KAFKA_HOST")
kafka_port = os.getenv("KAFKA_PORT")
kafka_topic = os.getenv('KAFKA_TOPIC')
kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS')

def send_to_status_service(order_details: order_dto):
    producer = KafkaProducer(bootstrap_servers=[kafka_bootstrap_servers], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    producer.send(kafka_topic, order_details.dict())
    producer.flush()
    producer.close()
    