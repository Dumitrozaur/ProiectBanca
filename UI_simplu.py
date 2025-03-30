import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox
from gestiune import *
from decimal import Decimal
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk

logged_user_id = None

def format_data(data):
    return [str(item).replace("Decimal('", "").replace("')", "").replace("'", "") for item in data]

# Funcție pentru verificarea login-ului
def check_login():
    global logged_user_id
    username = entry_username.get()
    password = entry_password.get()
    
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ClientID, Role FROM dbo.Users WHERE Username = ? AND PasswordHash = ?", (username, password))
            user = cursor.fetchone()
            if user:
                logged_user_id = user[0]
                role = user[1]
                login_window.destroy()
                if role == "admin":
                    admin_interface()
                else:
                    user_interface()
            else:
                messagebox.showerror("Eroare", "Username sau parolă incorectă.")
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la conectare: {e}")
        finally:
            conn.close()

# Creare fereastră de login
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x200")

ttk.Label(login_window, text="Username:").pack()
entry_username = ttk.Entry(login_window)
entry_username.pack()

ttk.Label(login_window, text="Password:").pack()
entry_password = ttk.Entry(login_window, show="*")
entry_password.pack()

btn_login = ttk.Button(login_window, text="Login", command=check_login)
btn_login.pack(pady=10)

# Funcție pentru interfața de admin
def user_interface():
    global show_content  # Ensure the function is accessible globally
    global logged_user_id
    root = tk.Tk()
    root.title("User Panel")
    root.geometry("800x600")

    ttk.Label(root, text="Interfața Utilizatorului", font=("Arial", 16)).pack(pady=10)

    # Butoane pentru acțiuni
    button_frame = ttk.Frame(root)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Vezi Loan", command=lambda: show_content("loan", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Solicită Împrumut", command=lambda: show_content("add_loan", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Vezi Date Personale", command=lambda: show_content("personal_data", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Transferă Bani", command=lambda: show_content("transfer", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Adaugă Fonduri", command=lambda: show_content("add_funds", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Vezi Conturi", command=lambda: show_content("view_accounts", content_frame)).pack(side=tk.LEFT, padx=10)
    ttk.Button(button_frame, text="Ieși", command=root.quit).pack(side=tk.LEFT, padx=10)

    # Creăm un Frame unde conținutul se va schimba
    content_frame = ttk.Frame(root)
    content_frame.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

def admin_interface():
    admin_window = tb.Window(themename="superhero")  # Poți schimba tema (ex: 'flatly', 'darkly', 'cyborg')
    admin_window.title("Admin Panel")
    admin_window.geometry("900x600")

    # Titlu
    title_label = ttk.Label(admin_window, text="Panou Administrator", font=("Arial", 20, "bold"))
    title_label.pack(pady=15)

    # Frame pentru butoane
    button_frame = ttk.Frame(admin_window)
    button_frame.pack(pady=20)

    # Butoane de acțiune
    buttons = [
        ("Gestionare Utilizatori", lambda: show_content("users")),
        ("Verifică Tranzacții", lambda: show_content("transactions")),
        ("Setări", lambda: show_content("settings")),
        ("Rapoarte Financiare", lambda: show_content("reports")),
        ("Deconectare", admin_window.quit)
    ]

    for text, command in buttons:
        btn = ttk.Button(button_frame, text=text, bootstyle="primary", command=command)
        btn.pack(fill=tk.X, pady=5, padx=20)

    # Frame pentru conținut dinamic
    content_frame = ttk.Frame(admin_window, borderwidth=2, relief="groove")
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def show_content(section):
        for widget in content_frame.winfo_children():
            widget.destroy()
        ttk.Label(content_frame, text=f"Conținut pentru {section}", font=("Arial", 14)).pack(pady=10)

    admin_window.mainloop()

def show_content(content_type, content_frame):
    # Curăță frame-ul de orice conținut existent
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    # Adăugăm noul conținut în funcție de butonul apăsat
    if content_type == "loan":
        view_loans(content_frame)
    elif content_type == "add_loan":
        add_loan(content_frame)
    elif content_type == "personal_data":
        view_personal_data(content_frame)
    elif content_type == "add_funds":
        add_funds(content_frame)
    elif content_type == "view_accounts":
        view_accounts(content_frame)
    elif content_type == "transfer":
        process_transfer(content_frame)


def view_accounts(content_frame):
    ttk.Label(content_frame, text="Conturile utilizatorului:").pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT AccountType, Balance, OpenDate FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            accounts = cursor.fetchall()

            style = ttk.Style()
            style.configure("Treeview", rowheight=30)
            style.configure("Treeview.Treeview", anchor="center")

            tree = ttk.Treeview(content_frame, columns=("Tip Cont", "Balanta", "Data Deschiderii"), show="headings")
            tree.heading("Tip Cont", text="Tip Cont")
            tree.heading("Balanta", text="Balanta")
            tree.heading("Data Deschiderii", text="Data Deschiderii")
            tree.pack(fill=tk.BOTH, expand=True)

            for account in accounts:
                tree.insert("", tk.END, values=format_data(account))
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea conturilor: {e}")
        finally:
            conn.close()

def add_funds(content_frame):
    ttk.Label(content_frame, text="Selectați contul în care doriți să adăugați fonduri:").pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT AccountID, AccountType FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            accounts = cursor.fetchall()

            account_options = [f"{account[1]} (ID: {account[0]})" for account in accounts]
            account_ids = [account[0] for account in accounts]

            account_combobox = ttk.Combobox(content_frame, values=account_options)
            account_combobox.pack(pady=10)

            ttk.Label(content_frame, text="Introduceți suma de adăugat:").pack(pady=10)
            entry_amount = ttk.Entry(content_frame)
            entry_amount.pack()

            def submit_funds():
                selected_account = account_combobox.get()
                amount = entry_amount.get()

                if not selected_account or not amount or not amount.isdigit() or float(amount) <= 0:
                    messagebox.showerror("Eroare", "Introducerea nu este validă!")
                    return

                amount = float(amount)
                selected_account_id = account_ids[account_options.index(selected_account)]

                try:
                    conn = getDBConnection()
                    if conn:
                        cursor = conn.cursor()
                        cursor.execute("UPDATE dbo.Accounts SET Balance = Balance + ? WHERE AccountID = ?", (amount, selected_account_id))
                        conn.commit()

                        messagebox.showinfo("Succes", f"Suma de {amount} a fost adăugată în contul {selected_account}!")
                        # Reîncarcă conturile
                        show_content("view_accounts", content_frame)
                except pyodbc.Error as e:
                    messagebox.showerror("Eroare", f"Eroare la adăugarea fondurilor: {e}")
                finally:
                    conn.close()
            ttk.Button(content_frame, text="Adaugă Fonduri", command=submit_funds).pack(pady=10)
            ttk.Button(content_frame, text="Anulează", command=lambda: show_content("view_accounts", content_frame)).pack(pady=10)
            ttk.Button(content_frame, text="Anulează", command=lambda: show_content("view_accounts")).pack(pady=10)
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea conturilor: {e}")
        finally:
            conn.close()

def view_loans(content_frame):
    ttk.Label(content_frame, text="Împrumuturile utilizatorului:").pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT LoanID, Amount, InterestRate, StartDate, EndDate, Status FROM dbo.Loans WHERE ClientID = ?", (logged_user_id,))
            loans = cursor.fetchall()

            # Treeview for loans
            tree = ttk.Treeview(content_frame, columns=("LoanID", "Sumă", "InterestRate", "Data Începerii", "Data Încheierii", "Status"), show="headings")
            tree.heading("LoanID", text="LoanID")
            tree.heading("Sumă", text="Sumă")
            tree.heading("InterestRate", text="InterestRate")
            tree.heading("Data Începerii", text="Data Începerii")
            tree.heading("Data Încheierii", text="Data Încheierii")
            tree.heading("Status", text="Status")
            tree.pack(fill=tk.BOTH, expand=True)

            for loan in loans:
                tree.insert("", tk.END, values=format_data(loan))

            ttk.Label(content_frame, text="Plăți asociate:").pack(pady=10)

            # Button for paying loan
            ttk.Button(content_frame, text="Plătește Împrumut", command=lambda: pay_loan(tree)).pack(pady=10)

            # Treeview for payments
            tree_payments = ttk.Treeview(content_frame, columns=("Suma Plătită", "Data Plății"), show="headings")
            tree_payments.heading("Suma Plătită", text="Suma Plătită")
            tree_payments.heading("Data Plății", text="Data Plății")
            tree_payments.pack(fill=tk.BOTH, expand=True)

            def load_payments(event):
                selected_item = tree.selection()
                if selected_item:
                    loan_id_str = tree.item(selected_item[0], "values")[0]  # Get the LoanID as a string
                    
                    try:
                        loan_id = int(loan_id_str)  # Convert LoanID to integer
                    except ValueError:
                        messagebox.showerror("Eroare", "ID-ul împrumutului este invalid!")
                        return
                    
                    # Execute the query with the loan_id as an integer
                    cursor.execute("SELECT AmountPaid, PaymentDate FROM dbo.LoanPayments WHERE LoanID = ?", (loan_id,))
                    payments = cursor.fetchall()

                    # Clear existing data
                    for item in tree_payments.get_children():
                        tree_payments.delete(item)

                    # Insert new payment data
                    for payment in payments:
                        tree_payments.insert("", tk.END, values=payment)

            tree.bind("<ButtonRelease-1>", load_payments)

            def pay_loan(tree):
                selected_item = tree.selection()
                if not selected_item:
                    messagebox.showerror("Eroare", "Selectați un împrumut pentru plată.")
                    return

                loan_id_str = tree.item(selected_item[0], "values")[0]
                try:
                    loan_id = int(loan_id_str)  # Convert LoanID to integer
                except ValueError:
                    messagebox.showerror("Eroare", "ID-ul împrumutului este invalid!")
                    return

                # Retrieve the loan amount and convert it properly
                amount_due_str = tree.item(selected_item[0], "values")[1]  # Sumă datorată
                try:
                    # Check if amount_due is of Decimal type and convert it to float
                    if isinstance(amount_due_str, Decimal):
                        amount_due = float(amount_due_str)
                    else:
                        # If it's a string, attempt to convert it to a float directly
                        amount_due = float(amount_due_str)
                except ValueError:
                    messagebox.showerror("Eroare", "Suma datorată nu este validă.")
                    return

                # Rest of the pay_loan logic...
                conn = getDBConnection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
                        account = cursor.fetchone()

                        if account:
                            account_balance = float(account[0])

                            # Verifică dacă utilizatorul are suficienți bani
                            if account_balance < amount_due:
                                messagebox.showerror("Eroare", "Sold insuficient pentru a efectua plata.")
                                return

                            # Dacă are suficienți bani, procedăm cu plata
                            pay_window = tk.Toplevel()
                            pay_window.title("Plată Împrumut")

                            ttk.Label(pay_window, text=f"Suma datorată: {amount_due}").pack()
                            ttk.Label(pay_window, text="Introduceți suma de plată:").pack()
                            entry_payment = ttk.Entry(pay_window)
                            entry_payment.pack()

                            ttk.Button(pay_window, text="Confirmă Plata", command=lambda: process_payment(tree, loan_id, amount_due, entry_payment)).pack(pady=10)

                            def process_payment(tree, loan_id, amount_due, entry_payment):
                                try:
                                    # Obținem suma plătită introdusă de utilizator
                                    amount_paid = float(entry_payment.get())

                                    # Verificăm dacă suma plătită este mai mare decât soldul contului
                                    conn = getDBConnection()
                                    cursor = conn.cursor()
                                    cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
                                    account = cursor.fetchone()

                                    if not account:
                                        messagebox.showerror("Eroare", "Contul utilizatorului nu a fost găsit.")
                                        return

                                    account_balance = float(account[0])

                                    if amount_paid > account_balance:
                                        messagebox.showerror("Eroare", "Sold insuficient pentru a efectua plata.")
                                        return

                                    # Dacă suma plătită este mai mică decât suma datorată
                                    if amount_paid < amount_due:
                                        cursor.execute("INSERT INTO dbo.LoanPayments (LoanID, AmountPaid, PaymentDate) VALUES (?, ?, GETDATE())", (loan_id, amount_paid))
                                        conn.commit()
                                        messagebox.showinfo("Succes", "Plata a fost înregistrată parțial.")
                                        show_content("loan", content_frame)  # Actualizează lista împrumuturilor
                                    else:
                                        # În cazul în care plata acoperă întreaga sumă datorată, ștergem împrumutul și plățile asociate
                                        cursor.execute("DELETE FROM dbo.LoanPayments WHERE LoanID = ?", (loan_id,))
                                        cursor.execute("DELETE FROM dbo.Loans WHERE LoanID = ?", (loan_id,))
                                        conn.commit()
                                        messagebox.showinfo("Succes", "Împrumutul a fost achitat și eliminat.")

                                    # Scădem suma plătită din soldul contului utilizatorului
                                    cursor.execute("UPDATE dbo.Accounts SET Balance = Balance - ? WHERE ClientID = ?", (amount_paid, logged_user_id))
                                    conn.commit()

                                    # Închidem conexiunea la baza de date
                                    conn.close()

                                    # Reîmprospătăm interfața
                                    tree.selection_set([])
                                    show_content("loan", content_frame)

                                except ValueError:
                                    messagebox.showerror("Eroare", "Introduceți o sumă validă pentru plată.")
                                except pyodbc.Error as e:
                                    messagebox.showerror("Eroare", f"Eroare la procesarea plății: {e}")

                    except pyodbc.Error as e:
                            messagebox.showerror("Eroare", f"Eroare la verificarea soldului: {e}")
                    finally:
                        print("Plata procesată.")

        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea împrumuturilor: {e}")
def add_loan(content_frame):
                ttk.Label(content_frame, text="Solicitare Împrumut").pack(pady=10)

                ttk.Label(content_frame, text="Introduceți detaliile împrumutului").pack(pady=10)

                ttk.Label(content_frame, text="Sumă:").pack()
                entry_amount = ttk.Entry(content_frame)
                entry_amount.pack()

                ttk.Label(content_frame, text="Rata Dobânzii (%):").pack()
                entry_interest = ttk.Entry(content_frame)
                entry_interest.pack()

                ttk.Label(content_frame, text="Data Începerii (YYYY-MM-DD):").pack()
                entry_start_date = ttk.Entry(content_frame)
                entry_start_date.pack()

                ttk.Label(content_frame, text="Data Încheierii (YYYY-MM-DD):").pack()
                entry_end_date = ttk.Entry(content_frame)
                entry_end_date.pack()

                def submit_loan():
                    amount = entry_amount.get()
                    interest = entry_interest.get()
                    start_date = entry_start_date.get()
                    end_date = entry_end_date.get()

                    if not amount or not interest or not start_date or not end_date:
                        messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii!")
                        return

                    try:
                        conn = getDBConnection()
                        if conn:
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO dbo.Loans (ClientID, Amount, InterestRate, StartDate, EndDate, Status) VALUES (?, ?, ?, ?, ?, ?)",
                                (logged_user_id, float(amount), float(interest), start_date, end_date, "Pending"),
                            )
                            conn.commit()
                            messagebox.showinfo("Succes", "Împrumut adăugat cu succes!")
            
                    except pyodbc.Error as e:
                        messagebox.showerror("Eroare", f"Eroare la adăugarea împrumutului: {e}")
                    finally:
                        if conn:
                            conn.close()

                ttk.Button(content_frame, text="Solicită Împrumut", command=submit_loan).pack(pady=10)

def process_transfer(content_frame):
    # Ștergem conținutul anterior din content_frame
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    ttk.Label(content_frame, text="Transferă Bani").pack(pady=10)

    # Crearea câmpului pentru ID-ul destinatarului
    ttk.Label(content_frame, text="ID destinatar:").pack(pady=5)
    entry_recipient = ttk.Entry(content_frame)
    entry_recipient.pack(pady=5)

    # Crearea câmpului pentru suma de transferat
    ttk.Label(content_frame, text="Sumă de transferat:").pack(pady=5)
    entry_amount = ttk.Entry(content_frame)
    entry_amount.pack(pady=5)

    # Crearea unui buton pentru a efectua transferul
    transfer_button = ttk.Button(content_frame, text="Transferă", 
                                 command=lambda: execute_transfer(entry_recipient, entry_amount, content_frame))
    transfer_button.pack(pady=20)

# Funcția care execută efectiv transferul când apăsăm pe buton
def execute_transfer(entry_recipient, entry_amount, content_frame):
    recipient_id = entry_recipient.get().strip()  # Eliminăm spațiile goale
    amount = entry_amount.get().strip()

    # Validare: ID-ul destinatarului și suma trebuie să fie numere valide
    if not recipient_id.isdigit() or not amount.replace('.', '', 1).isdigit():
        messagebox.showerror("Eroare", "ID-ul destinatarului sau suma sunt invalide!")
        return

    amount = float(amount)

    # Obținem soldul contului utilizatorului logat
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()

            # Verificăm soldul utilizatorului curent
            cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            account = cursor.fetchone()

            if not account:
                messagebox.showerror("Eroare", "Nu s-a putut obține soldul contului!")
                return

            account_balance = float(account[0])

            # Verificăm dacă utilizatorul are suficienți bani
            if account_balance < amount:
                messagebox.showerror("Eroare", "Sold insuficient pentru a efectua transferul.")
                return

            # Verificăm dacă ID-ul destinatarului există
            cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (recipient_id,))
            recipient_account = cursor.fetchone()

            if not recipient_account:
                messagebox.showerror("Eroare", "Destinatarul nu există în baza de date.")
                return

            # Executăm transferul:
            cursor.execute("UPDATE dbo.Accounts SET Balance = Balance - ? WHERE ClientID = ?", (amount, logged_user_id))
            cursor.execute("UPDATE dbo.Accounts SET Balance = Balance + ? WHERE ClientID = ?", (amount, recipient_id))

            # Salvăm transferul în tabelul Transfers
            cursor.execute("INSERT INTO dbo.Transfers (FromAccountID, ToAccountID, Amount, TransferDate) VALUES (?, ?, ?, GETDATE())",
                           (logged_user_id, recipient_id, amount))

            # Confirmăm tranzacția în baza de date
            conn.commit()

            # Mesaj de succes
            messagebox.showinfo("Succes", f"Transfer de {amount} realizat către utilizatorul {recipient_id}.")

            # Reîncărcăm pagina de vizualizare a contului
            show_content("view_accounts", content_frame)

        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la procesarea transferului: {e}")
        finally:
            conn.close()

def view_personal_data(content_frame):
    ttk.Label(content_frame, text="Datele personale:").pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Username, PasswordHash, Role FROM dbo.Users WHERE ClientID = ?", (logged_user_id,))
            user_data = cursor.fetchone()

            if user_data:
                ttk.Label(content_frame, text="Datele personale:").pack(pady=10)
                ttk.Label(content_frame, text=f"Username: {user_data[0]}").pack()
                ttk.Label(content_frame, text=f"Password: {user_data[1]}").pack()
                ttk.Label(content_frame, text=f"Role: {user_data[2]}").pack()
            else:
                messagebox.showinfo("Info", "Nu s-au găsit date personale.")
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea datelor personale: {e}")
        finally:
            conn.close()

login_window.mainloop()
