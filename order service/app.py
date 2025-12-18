from service.order_service import create_order
from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from Models.orders import order
from Dto.order_dto  import order_dto
from db.dbConnection import getConnection
from db.execute import executeScriptWithoutReturn, executeScriptWithReturn
from typing import Dict, Any
import json

app = FastAPI()


@app.get("/order/{order_id}")
async def getOrders(order_id):
    query = "select * from orders where id = %s"
    response = await executeScriptWithReturn(query=query, params=[order_id])
    
    return response


@app.post('/order')
async def newOrder(order: order_dto):
    res = await create_order(order)
    return res
    

@app.put('/order/{order_id}')
async def updateOrder(order_id, order_details:order_dto):
    columns = ''
    params = [order_details.user_id, order_details.price, 
              order_details.currency, json.dumps({'source': order_details.source, 'payment_method': order_details.payment_method}),
              order_id]
    query = 'UPDATE orders SET user_id = %s,  total_amount = %s, currency = %s, metadata = %s where id = %s'
    response = await executeScriptWithoutReturn(query= query, params=params)
    return response

        
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
    