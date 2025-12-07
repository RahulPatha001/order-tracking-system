
from db.dbConnection import getConnection
from fastapi import HTTPException

def executeScript(query: str, params):
    # db connections
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute(query=query, params=params)
        row= cur.fetchone()
        conn.commit()
    except Exception as e:
        conn.rollback()
        # You can log e here
        raise HTTPException(status_code=500, detail="Failed to create order")
    finally:
        cur.close()
        conn.close()

