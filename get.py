import pyodbc
from gestiune import *

def get_clients():
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName FROM dbo.Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients
    return []