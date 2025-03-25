import tkinter as tk
from tkinter import messagebox

def validate_login():
    username = username_entry.get()
    password = password_entry.get()
    
    # Logica de validare a login-ului
    if username == "admin" and password == "1234":
        messagebox.showinfo("Login Success", "Admin logged in successfully!")
        # Aici vei apela funcționalitatea Adminului
        # show_clients() 
    elif username == "user" and password == "abcd":
        messagebox.showinfo("Login Success", "User logged in successfully!")
        # Aici vei apela funcționalitatea Userului
        # show_user_dashboard() 
    else:
        messagebox.showerror("Login Failed", "Invalid username or password!")

root = tk.Tk()
root.title("Bank Login")
root.geometry("300x200")

tk.Label(root, text="Login", font=("Arial", 12)).pack(pady=10)

tk.Label(root, text="Username:").pack()
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack(pady=5)

tk.Button(root, text="Login", command=validate_login).pack(pady=10)

root.mainloop()
