from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from Models.orders import order
from db.dbConnection import getConnection
from db.execute import executeScript
from typing import Dict, Any

app = FastAPI()


@app.get("/order/{order_id}")
def getOrders(order_id):
    query = "select * from orders where id = %s"
    response = executeScript(query=query, params=order_id)
    
    return response


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

@app.put('/order/{order_id}')
def updateOrder(order_id, order_details:Dict[str, Any]):
    
    query = "Update orders set status = %s, updated_at= %s where id = %s"
    if not order_details["status"] or not order_details["updated_at"]:
        raise HTTPException(status_code=404, detail="required information is not found")
    params = [order_details["status"], order_details["updated_at"], order_id]    
    response = executeScript(params=params, query=query)
    print(response)
    
    try:
        updated_response = executeScript("select * from orders where id = %s", order_id)
        return updated_response
    except Exception as e:
        print(e)
    