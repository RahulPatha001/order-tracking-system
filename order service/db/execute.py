
from db.dbConnection import getConnection
from fastapi import HTTPException
import traceback

def executeScript(query: str, params):
    # db connections
    conn = getConnection()
    cur = conn.cursor()

    try:
        cur.execute(query, params)
        conn.commit()
        columns = [col[0] for col in cur.description]
        result= cur.fetchone()
        print( cur.description[0])
        return dict(zip(columns, result))
    except Exception as e:
        conn.rollback()
        print(f"Database error: {e}")
        traceback.print_exc()
        # You can log e here
        raise HTTPException(status_code=500, detail="Failed to create order")
    finally:
        cur.close()
        conn.close()

