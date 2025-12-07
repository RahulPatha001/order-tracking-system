import psycopg2


def getConnection():
    return psycopg2.connect(
    dbname="orders",
    user="root",
    password="rahul.123*",
    host="localhost",
    port=5433,
)
    


