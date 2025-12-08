from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from Models.orders import order
from db.dbConnection import getConnection
from db.execute import executeScript

app = FastAPI()


@app.get("/order/{order_id}")
def getOrders(order_id: int):
    return 'order'


@app.post('/order')
def newOrder(order: order):
    fields =["user_id", "status"]
    values = [order.user_id, order.status]
    
    if order.created_at is not None:
        fields.append("created_at")
        values.append(order.created_at)
        
    if order.updated_at is not None:
        fields.append("updated_at")
        values.append(order.updated_at)
    
    field_names = ', '.join(fields)
    placeholders = ', '.join(['%s'] * len(values))
        
    query = f"INSERT INTO orders ({field_names}) VALUES ({placeholders}) RETURNING *"
    response = executeScript(query=query, params=tuple(values))
    print(response)
    
    return response
    
    
    