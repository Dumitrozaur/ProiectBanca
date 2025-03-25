import pyodbc
import tkinter as tk
from tkinter import ttk
from gestiune import *
from get import *
from insert import * 

def get_clients():
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName, DOB, Email, PhoneNumber, Address FROM dbo.Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients
    return []

root = tk.Tk()
root.title("Bank Client Management")
root.geometry("500x300")

frame = ttk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree = ttk.Treeview(frame, columns=("ID", "Nume", "Prenume", "Data de Nastere", "Email", "Numar de Telefon", "Adresa"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nume", text="Nume")
tree.heading("Prenume", text="Prenume")
tree.heading("Data de Nastere", text="Data de Nastere")
tree.heading("Email", text="Email")
tree.heading("Numar de Telefon", text="Numar de Telefon")
tree.heading("Adresa", text="Adresa")

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)

# Încărcare date
for client in get_clients():
    tree.insert("", "end", values=client)

root.mainloop()
