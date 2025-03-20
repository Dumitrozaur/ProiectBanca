import pyodbc

SERVER_NAME = "DESKTOP-AS1QGLB"
DATABASE_NAME = "BankDB"
CONN_STRING = f"DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

try:
    conn = pyodbc.connect(CONN_STRING)
    cursor = conn.cursor()
    print("Connection successful!")

    SQL_STATEMENT = """
    INSERT INTO dbo.Clients (
        FirstName, 
        LastName, 
        DOB, 
        Email, 
        PhoneNumber,
        Address
    ) OUTPUT INSERTED.ClientID
    VALUES (?, ?, ?, ?, ?, ?)
    """

    data = (
        'John',                 # FirstName
        'Doe',                  # LastName
        '1990-05-14',           # DOB (YYYY-MM-DD format)
        'john.doe@example.com', # Email
        '123-456-7890',         # PhoneNumber
        '123 Elm Street'        # Address
    )

    cursor.execute(SQL_STATEMENT, data)
    new_client_id = cursor.fetchone()[0]
    print(f"Inserted new client with ID: {new_client_id}")

    conn.commit()

except pyodbc.Error as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    conn.close()
    print("Connection closed.")
