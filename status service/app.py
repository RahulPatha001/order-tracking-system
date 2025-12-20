from service.kafka_consumer import KafkaConsumer
from fastapi import FastAPI

app = FastAPI()

KafkaConsumer()