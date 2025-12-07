from fastapi import FastAPI
from Models.orders import order
from db.dbConnection import getConnection

app = FastAPI()


@app.get("/order/{order_id}")
def getOrders(order_id: int):
    return 'order'


@app.post('/order')
def newOrder(order: order):
    
    
    