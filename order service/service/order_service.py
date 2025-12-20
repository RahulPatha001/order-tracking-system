import uuid
from Dto.order_dto import order_dto
from Models.orders import order,order_items
from fastapi import HTTPException
from db.execute import executeScriptWithoutReturn
from service.kafkaProducer import send_to_status_service
import json

async def create_order(order_obj: order_dto):
    order_to_store = order(  
        user_id=order_obj.user_id,
        currency=order_obj.currency,
        status='PLACED',
        metadata=json.dumps({"source": order_obj.source, "payment_method": order_obj.payment_method}),
        trace_id=str(uuid.uuid4()),
        total_amount=order_obj.price
    )
    print(order_to_store)

    # inserting into orders table
    query = "INSERT INTO orders (user_id, currency, status, metadata, trace_id, total_amount) VALUES (%s, %s, %s, %s, %s, %s) returning id"
    try:
        response = await executeScriptWithoutReturn(query, (  
            order_to_store.user_id, order_to_store.currency, 
            order_to_store.status, json.dumps(order_to_store.metadata), 
            order_to_store.trace_id, order_to_store.total_amount
        ))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to create order")
    
    order_id = response[0]
    print(type(order_id))

    # inserting into order_items table

    items = list(order_obj.items.keys())
    for item in items:
        query = "INSERT INTO order_items (order_id, sku, name, qty, price) VALUES (%s, %s, %s, %s, %s) returning id"
        try:
            await executeScriptWithoutReturn(query, (order_id, "sku123", item, order_obj.items[item], int(order_obj.price)))
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Failed to create order")
    send_to_status_service(order_details=order_obj)
    return order_id




