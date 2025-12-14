from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from Models.orders import order
from Dto.order_dto  import order_dto
from db.dbConnection import getConnection
from db.execute import executeScriptWithoutReturn, executeScriptWithReturn
from typing import Dict, Any

app = FastAPI()


@app.get("/order/{order_id}")
def getOrders(order_id):
    query = "select * from orders where id = %s"
    response = executeScriptWithReturn(query=query, params=order_id)
    
    return response


@app.post('/order')
def newOrder(order: order_dto):
    return order
    

@app.put('/order/{order_id}')
def updateOrder(order_id, order_details:Dict[str, Any]):
    
    query = "Update orders set status = %s, updated_at= %s where id = %s"
    if not order_details["status"] or not order_details["updated_at"]:
        raise HTTPException(status_code=404, detail="required information is not found")
    params = [order_details["status"], order_details["updated_at"], order_id]    
    response = executeScriptWithoutReturn(params=params, query=query)
    print(response)
    
    try:
        updated_response = executeScriptWithoutReturn("select * from orders where id = %s", order_id)
        return updated_response
    except Exception as e:
        print(e)
        
@app.delete('/order/{order_id}')
def deleteOrder(order_id):
    query = 'delete from orders where id = %s'
    if not order_id:
        raise HTTPException(status_code=404, detail="ID is not provided")
    try:
        response = executeScriptWithoutReturn(query=query, params=[order_id])
        return response
    except Exception as e:
        print(e)
    