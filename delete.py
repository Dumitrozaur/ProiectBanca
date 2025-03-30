import pyodbc
from gestiune import *

def delete_function(ID, tableName):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM dbo.{tableName} WHERE {tableName}ID = {ID}")
            conn.commit()
            print(f"{tableName} deleted successfully from dataBase")
        except pyodbc.Error as e:
            print(f"Error deleting {tableName} from database: {e}")
        finally:
            conn.close()


            
