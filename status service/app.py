from service.kafka_consumer import order_consumer
from fastapi import FastAPI

app = FastAPI()

order_consumer()