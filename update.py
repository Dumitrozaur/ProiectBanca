import pydoc
from gestiune import *

def update_table(tablename, record_id, column, new_value, id_column):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql_update = f"UPDATE dbo.{tablename} SET {column} = ? WHERE {id_column} = ?"
            cursor.execute(sql_update, (new_value, record_id))
            conn.commit()
            print(f"{tablename} updated successfully in database")
        except pyodbc.Error as e:
            print(f"Error updating {tablename} in database: {e}")
        finally:
            conn.close()

#update_table("Clients", 1, "FirstName", "Gone", "ClientID")
