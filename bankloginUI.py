import tkinter as tk
from tkinter import messagebox

def login(user_type):
    login_window = tk.Toplevel(root)
    login_window.title(f"Login - {user_type}")
    login_window.geometry("300x200")
    
    tk.Label(login_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=5)
    
    tk.Label(login_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=5)
    
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()
        if user_type == "Admin" and username == "admin" and password == "1234":
            messagebox.showinfo("Login Success", "Admin logged in successfully!")
        elif user_type == "User" and username == "user" and password == "abcd":
            messagebox.showinfo("Login Success", "User logged in successfully!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")
    
    tk.Button(login_window, text="Login", command=validate_login).pack(pady=10)

root = tk.Tk()
root.title("Bank Login")
root.geometry("300x200")

tk.Label(root, text="Select Login Type:", font=("Arial", 12)).pack(pady=10)

tk.Button(root, text="Login as Admin", command=lambda: login("Admin"), width=20).pack(pady=5)

tk.Button(root, text="Login as User", command=lambda: login("User"), width=20).pack(pady=5)

root.mainloop()
