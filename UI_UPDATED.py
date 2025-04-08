import pyodbc
import tkinter as tk
from tkinter import ttk, messagebox
from gestiune import *
from decimal import Decimal
import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk
import datetime


def format_data(data):
    return [str(item).replace("Decimal('", "").replace("')", "").replace("'", "") for item in data]

logged_user_id = None


def admin_interface():
    admin_window = tb.Window(themename="superhero")  
    admin_window.title("Admin Panel")
    admin_window.geometry("900x600")

    title_label = ttk.Label(admin_window, text="Panou Administrator", font=("Arial", 20, "bold"))
    title_label.pack(pady=15)


    button_frame = ttk.Frame(admin_window)
    button_frame.pack(pady=20)

    buttons = [
        ("Gestionare Utilizatori", lambda: show_users_table(content_frame)),
        ("Verifică Tranzacții", lambda: show_transactions(content_frame)),
        ("Deconectare", admin_window.quit)
    ]

    for text, command in buttons:
        btn = ttk.Button(button_frame, text=text, bootstyle="primary", command=command)
        btn.pack(fill=tk.X, pady=5, padx=20)


    content_frame = ttk.Frame(admin_window, borderwidth=2, relief="groove", padding=20)
    content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    admin_window.mainloop()

def show_transactions(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(content_frame, columns=("ID", "From", "To", "Amount", "Date"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("From", text="From")
    tree.heading("To", text="To")
    tree.heading("Amount", text="Sumă")
    tree.heading("Date", text="Dată")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = getDBConnection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT TransferID, FromAccountID, ToAccountID, Amount, TransferDate FROM dbo.Transfers")
        transactions = cursor.fetchall()

        for transaction in transactions:
            tree.insert('', tk.END, values=format_data(transaction))
    
    except Exception as e:
        messagebox.showerror("Eroare", f"Eroare la încărcarea tranzacțiilor: {e}")
    
    finally:
        conn.close()

def show_users_table(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    tree = ttk.Treeview(content_frame, columns=("ID", "Nume", "Email"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Nume", text="Nume")
    tree.heading("Email", text="Email")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ClientID, FirstName, Email FROM dbo.Clients")
            rows = cursor.fetchall()
            for row in rows:
                formatted_row = format_data(row)
                tree.insert('', tk.END, values=formatted_row)
        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la extragerea clienților: {e}")
        finally:
            conn.close()

    def on_user_select(event):
        selected = tree.focus()
        values = tree.item(selected, 'values')
        if values:
            show_user_details(content_frame, user_id=values[0])

    tree.bind("<<TreeviewSelect>>", on_user_select)

def show_user_details(content_frame, user_id):
    for widget in content_frame.winfo_children():
        widget.destroy()

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT FirstName, LastName, DOB, Email, PhoneNumber, Address FROM dbo.Clients WHERE ClientID = ?", (user_id,))
            user = cursor.fetchone()

            if user:
                def format_data(user):
                    first_name, last_name, dob, email, phone, address = user
                    dob = user[2]

                    formatted_email = email.lower() if email else "N/A"

                    return [first_name, last_name, dob, formatted_email, phone, address]
                formatted_data = format_data(user)

                labels = ["Prenume", "Nume", "Data nașterii", "Email", "Telefon", "Adresă"]

                for label, value in zip(labels, formatted_data):
                    ttk.Label(content_frame, text=f"{label}: {value}", font=("Arial", 12)).pack(anchor="w", padx=10, pady=2)

                def save_changes(user_id, name_var, last_name_var, email_var, phone_var, content_frame, conn, cursor):
                    if cursor is None:
                        conn = getDBConnection()
                        cursor = conn.cursor()

                    new_name = name_var.get().strip()
                    new_last_name = last_name_var.get().strip()
                    new_email = email_var.get().strip()
                    new_phone = phone_var.get().strip()

                    if not new_name or not new_last_name or not new_email or not new_phone:
                        messagebox.showerror("Eroare", "Toate câmpurile trebuie completate.")
                        return

                    if "@" not in new_email:
                        messagebox.showerror("Eroare", "Email-ul nu este valid.")
                        return

                    try:
                        cursor.execute("""UPDATE dbo.Clients 
                                           SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ? 
                                           WHERE ClientID = ?""", 
                                       (new_name, new_last_name, new_email, new_phone, user_id))
                        conn.commit()
                        messagebox.showinfo("Succes", "Datele au fost actualizate cu succes.")
                        show_users_table(content_frame) 
                    except Exception as e:
                        messagebox.showerror("Eroare", f"Eroare la actualizare: {e}")
                    finally:
                        conn.close()

                name_var = tk.StringVar(value=formatted_data[0])
                last_name_var = tk.StringVar(value=formatted_data[1])
                email_var = tk.StringVar(value=formatted_data[3])
                phone_var = tk.StringVar(value=formatted_data[4])

                ttk.Label(content_frame, text="Prenume:").pack(anchor="w", padx=10)
                ttk.Entry(content_frame, textvariable=name_var, font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

                ttk.Label(content_frame, text="Nume:").pack(anchor="w", padx=10)
                ttk.Entry(content_frame, textvariable=last_name_var, font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

                ttk.Label(content_frame, text="Email:").pack(anchor="w", padx=10)
                ttk.Entry(content_frame, textvariable=email_var, font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

                ttk.Label(content_frame, text="Telefon:").pack(anchor="w", padx=10)
                ttk.Entry(content_frame, textvariable=phone_var, font=("Arial", 12)).pack(anchor="w", padx=10, pady=5)

                ttk.Button(content_frame, text="Salvează modificările", 
                           command=lambda: save_changes(user_id, name_var, last_name_var, email_var, phone_var, content_frame, conn, cursor)).pack(pady=10)

        except Exception as e:
            messagebox.showerror("Eroare", f"Eroare la extragerea datelor: {e}")
        finally:
            pass

def show_content(content_type, content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    content_label = ttk.Label(content_frame, text=f"Încărcare {content_type.capitalize()}", font=("Arial", 14, "italic"))
    content_label.pack(pady=10, padx=20)

    inner_frame = ttk.Frame(content_frame, relief="groove", borderwidth=2, padding=20)
    inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    if content_type == "loan":
        view_loans(inner_frame)
    elif content_type == "add_loan":
        add_loan(inner_frame)
    elif content_type == "personal_data":
        view_personal_data(inner_frame)
    elif content_type == "add_funds":
        add_funds(inner_frame)
    elif content_type == "view_accounts":
        view_accounts(inner_frame)
    elif content_type == "transfer":
        process_transfer(inner_frame)


def view_accounts(content_frame):
    ttk.Label(content_frame, text="Conturile utilizatorului:", font=("Arial", 16, "bold")).pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT AccountType, Balance, OpenDate FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            accounts = cursor.fetchall()

            style = ttk.Style()
            style.configure("Treeview", rowheight=30, font=("Arial", 12))
            style.configure("Treeview.Heading", font=("Arial", 12, "bold"), foreground="blue")
            style.configure("Treeview.Treeview", anchor="center", background="lightgrey", foreground="black")

            tree = ttk.Treeview(content_frame, columns=("Tip Cont", "Balanta", "Data Deschiderii"), show="headings")
            tree.heading("Tip Cont", text="Tip Cont")
            tree.heading("Balanta", text="Balanta")
            tree.heading("Data Deschiderii", text="Data Deschiderii")

            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            for account in accounts:
                tree.insert("", tk.END, values=format_data(account))

        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea conturilor: {e}")
        finally:
            conn.close()

def add_funds(content_frame):
    ttk.Label(content_frame, text="Selectați contul în care doriți să adăugați fonduri:", font=("Arial", 16, "bold")).pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT AccountID, AccountType FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            accounts = cursor.fetchall()

            account_options = [f"{account[1]} (ID: {account[0]})" for account in accounts]
            account_ids = [account[0] for account in accounts]

            account_combobox = ttk.Combobox(content_frame, values=account_options, width=30, font=("Arial", 12))
            account_combobox.set("Selectați contul")
            account_combobox.pack(pady=10)

            ttk.Label(content_frame, text="Introduceți suma de adăugat:", font=("Arial", 14)).pack(pady=10)
            entry_amount = ttk.Entry(content_frame, font=("Arial", 12))
            entry_amount.pack(pady=5)

            def submit_funds():
                selected_account = account_combobox.get()
                amount = entry_amount.get()

                if not selected_account or not amount or not amount.isdigit() or float(amount) <= 0:
                    messagebox.showerror("Eroare", "Introducerea nu este validă! Asigurați-vă că suma este validă și mai mare decât 0.")
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
                        show_content("view_accounts", content_frame)
                except pyodbc.Error as e:
                    messagebox.showerror("Eroare", f"Eroare la adăugarea fondurilor: {e}")
                finally:
                    conn.close()

            ttk.Button(content_frame, text="Adaugă Fonduri", command=submit_funds, bootstyle="success", width=20).pack(pady=15)

            cancel_button = ttk.Button(content_frame, text="Anulează", command=lambda: show_content("view_accounts", content_frame), bootstyle="danger", width=20)
            cancel_button.pack(pady=5)

        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea conturilor: {e}")
        finally:
            conn.close()


def view_loans(content_frame):
    ttk.Label(content_frame, text="Împrumuturile utilizatorului:", font=("Arial", 16, "bold")).pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT LoanID, Amount, InterestRate, StartDate, EndDate, Status FROM dbo.Loans WHERE ClientID = ?", (logged_user_id,))
            loans = cursor.fetchall()

            style = ttk.Style()
            style.configure("Treeview", rowheight=30, font=("Arial", 12))  # Stilizare Treeview
            tree = ttk.Treeview(content_frame, columns=("LoanID", "Sumă", "InterestRate", "Data Începerii", "Data Încheierii", "Status"), show="headings")
            tree.heading("LoanID", text="LoanID")
            tree.heading("Sumă", text="Sumă")
            tree.heading("InterestRate", text="InterestRate")
            tree.heading("Data Începerii", text="Data Începerii")
            tree.heading("Data Încheierii", text="Data Încheierii")
            tree.heading("Status", text="Status")
            tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            for loan in loans:
                tree.insert("", tk.END, values=format_data(loan))

            ttk.Label(content_frame, text="Plăți asociate:", font=("Arial", 14)).pack(pady=10)

            ttk.Button(content_frame, text="Plătește Împrumut", command=lambda: pay_loan(tree), bootstyle="success", width=20).pack(pady=10)

            tree_payments = ttk.Treeview(content_frame, columns=("Suma Plătită", "Data Plății"), show="headings")
            tree_payments.heading("Suma Plătită", text="Suma Plătită")
            tree_payments.heading("Data Plății", text="Data Plății")
            tree_payments.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

            def load_payments(event):
                selected_item = tree.selection()
                if selected_item:
                    loan_id_str = tree.item(selected_item[0], "values")[0] 

                    try:
                        loan_id = int(loan_id_str) 
                    except ValueError:
                        messagebox.showerror("Eroare", "ID-ul împrumutului este invalid!")
                        return

                    cursor.execute("SELECT AmountPaid, PaymentDate FROM dbo.LoanPayments WHERE LoanID = ?", (loan_id,))
                    payments = cursor.fetchall()

                    for item in tree_payments.get_children():
                        tree_payments.delete(item)

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
                    loan_id = int(loan_id_str) 
                except ValueError:
                    messagebox.showerror("Eroare", "ID-ul împrumutului este invalid!")
                    return

                amount_due_str = tree.item(selected_item[0], "values")[1] 
                try:
                    if isinstance(amount_due_str, Decimal):
                        amount_due = float(amount_due_str)
                    else:
                        amount_due = float(amount_due_str)
                except ValueError:
                    messagebox.showerror("Eroare", "Suma datorată nu este validă.")
                    return

                conn = getDBConnection()
                if conn:
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
                        account = cursor.fetchone()

                        if account:
                            account_balance = float(account[0])

                            if account_balance < amount_due:
                                messagebox.showerror("Eroare", "Sold insuficient pentru a efectua plata.")
                                return

                            pay_window = tk.Toplevel()
                            pay_window.title("Plată Împrumut")
                            ttk.Label(pay_window, text=f"Suma datorată: {amount_due}", font=("Arial", 14)).pack(pady=10)
                            ttk.Label(pay_window, text="Introduceți suma de plată:", font=("Arial", 12)).pack(pady=5)
                            entry_payment = ttk.Entry(pay_window, font=("Arial", 12))
                            entry_payment.pack(pady=10)

                            ttk.Button(pay_window, text="Confirmă Plata", command=lambda: process_payment(tree, loan_id, amount_due, entry_payment), bootstyle="success").pack(pady=10)

                            def process_payment(tree, loan_id, amount_due, entry_payment):
                                try:
                                    amount_paid = float(entry_payment.get())

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

                                    if amount_paid < amount_due:
                                        cursor.execute("INSERT INTO dbo.LoanPayments (LoanID, AmountPaid, PaymentDate) VALUES (?, ?, GETDATE())", (loan_id, amount_paid))
                                        conn.commit()
                                        messagebox.showinfo("Succes", "Plata a fost înregistrată parțial.")
                                        show_content("loan", content_frame)
                                    else:
                                        cursor.execute("DELETE FROM dbo.LoanPayments WHERE LoanID = ?", (loan_id,))
                                        cursor.execute("DELETE FROM dbo.Loans WHERE LoanID = ?", (loan_id,))
                                        conn.commit()
                                        messagebox.showinfo("Succes", "Împrumutul a fost achitat și eliminat.")

                                    cursor.execute("UPDATE dbo.Accounts SET Balance = Balance - ? WHERE ClientID = ?", (amount_paid, logged_user_id))
                                    conn.commit()
                                    conn.close()

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
    ttk.Label(content_frame, text="Solicitare Împrumut", font=("Arial", 16, "bold")).pack(pady=10)

    ttk.Label(content_frame, text="Introduceți detaliile împrumutului", font=("Arial", 14)).pack(pady=10)

    ttk.Label(content_frame, text="Sumă:", font=("Arial", 12)).pack(pady=5)
    entry_amount = ttk.Entry(content_frame, font=("Arial", 12))
    entry_amount.pack(pady=5)

    ttk.Label(content_frame, text="Rata Dobânzii (%):", font=("Arial", 12)).pack(pady=5)
    entry_interest = ttk.Entry(content_frame, font=("Arial", 12))
    entry_interest.pack(pady=5)

    ttk.Label(content_frame, text="Data Începerii (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=5)
    entry_start_date = ttk.Entry(content_frame, font=("Arial", 12))
    entry_start_date.pack(pady=5)

    ttk.Label(content_frame, text="Data Încheierii (YYYY-MM-DD):", font=("Arial", 12)).pack(pady=5)
    entry_end_date = ttk.Entry(content_frame, font=("Arial", 12))
    entry_end_date.pack(pady=5)

    def submit_loan():
        amount = entry_amount.get()
        interest = entry_interest.get()
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()

        if not amount or not interest or not start_date or not end_date:
            messagebox.showerror("Eroare", "Toate câmpurile sunt obligatorii!")
            return

        if not amount.isdigit() or float(amount) <= 0:
            messagebox.showerror("Eroare", "Suma introdusă nu este validă!")
            return
        if not interest.replace('.', '', 1).isdigit() or float(interest) < 0:
            messagebox.showerror("Eroare", "Rata dobânzii introdusă nu este validă!")
            return

        try:
            datetime.datetime.strptime(start_date, "%Y-%m-%d")
            datetime.datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Eroare", "Formatele datelor sunt invalide! Utilizați YYYY-MM-DD.")
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

    ttk.Button(content_frame, text="Solicită Împrumut", command=submit_loan, bootstyle="success", width=20).pack(pady=10)

def process_transfer(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()
    
    ttk.Label(content_frame, text="Transferă Bani", font=("Arial", 16, "bold")).pack(pady=10)

    ttk.Label(content_frame, text="ID destinatar:", font=("Arial", 12)).pack(pady=5)
    entry_recipient = ttk.Entry(content_frame, font=("Arial", 12))
    entry_recipient.pack(pady=5)

    ttk.Label(content_frame, text="Sumă de transferat:", font=("Arial", 12)).pack(pady=5)
    entry_amount = ttk.Entry(content_frame, font=("Arial", 12))
    entry_amount.pack(pady=5)

    def execute_transfer(entry_recipient, entry_amount, content_frame):
        recipient_id = entry_recipient.get()
        amount = entry_amount.get()

        if not recipient_id or not amount:
            messagebox.showerror("Eroare", "Ambele câmpuri sunt obligatorii!")
            return

        if not recipient_id.isdigit():
            messagebox.showerror("Eroare", "ID-ul destinatarului trebuie să fie un număr valid!")
            return
        
        if not amount.replace('.', '', 1).isdigit() or float(amount) <= 0:
            messagebox.showerror("Eroare", "Suma de transferat nu este validă!")
            return

        amount = float(amount)

        try:
            conn = getDBConnection()
            if conn:
                cursor = conn.cursor()

                cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
                account = cursor.fetchone()

                if account:
                    account_balance = float(account[0])

                    if account_balance < amount:
                        messagebox.showerror("Eroare", "Sold insuficient pentru a efectua transferul.")
                        return

                    cursor.execute("SELECT AccountID FROM dbo.Accounts WHERE ClientID = ?", (recipient_id,))
                    recipient_account = cursor.fetchone()

                    if not recipient_account:
                        messagebox.showerror("Eroare", "ID-ul destinatarului nu este valid!")
                        return

                    cursor.execute("UPDATE dbo.Accounts SET Balance = Balance - ? WHERE ClientID = ?", (amount, logged_user_id))
                    cursor.execute("UPDATE dbo.Accounts SET Balance = Balance + ? WHERE ClientID = ?", (amount, recipient_id))
                    conn.commit()

                    messagebox.showinfo("Succes", f"Transferul de {amount} către ID-ul {recipient_id} a fost realizat cu succes!")

                    show_content("view_accounts", content_frame)
                
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la procesarea transferului: {e}")
        finally:
            if conn:
                conn.close()

    transfer_button = ttk.Button(content_frame, text="Transferă", bootstyle="success", width=20, command=lambda: execute_transfer(entry_recipient, entry_amount, content_frame))
    transfer_button.pack(pady=20)

def execute_transfer(entry_recipient, entry_amount, content_frame):
    recipient_id = entry_recipient.get().strip()  # Eliminăm spațiile goale
    amount = entry_amount.get().strip()

    if not recipient_id.isdigit() or not amount.replace('.', '', 1).isdigit():
        messagebox.showerror("Eroare", "ID-ul destinatarului sau suma sunt invalide!")
        return

    amount = float(amount)

    if amount <= 0:
        messagebox.showerror("Eroare", "Suma de transferat trebuie să fie mai mare decât 0!")
        return

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()

            cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (logged_user_id,))
            account = cursor.fetchone()

            if not account:
                messagebox.showerror("Eroare", "Nu s-a putut obține soldul contului!")
                return

            account_balance = float(account[0])

            if account_balance < amount:
                messagebox.showerror("Eroare", "Sold insuficient pentru a efectua transferul.")
                return

            cursor.execute("SELECT Balance FROM dbo.Accounts WHERE ClientID = ?", (recipient_id,))
            recipient_account = cursor.fetchone()

            if not recipient_account:
                messagebox.showerror("Eroare", "Destinatarul nu există în baza de date.")
                return

            confirm = messagebox.askyesno("Confirmare", f"Doriți să transferați {amount} către utilizatorul {recipient_id}?")
            if not confirm:
                return

            cursor.execute("UPDATE dbo.Accounts SET Balance = Balance - ? WHERE ClientID = ?", (amount, logged_user_id))
            cursor.execute("UPDATE dbo.Accounts SET Balance = Balance + ? WHERE ClientID = ?", (amount, recipient_id))

            cursor.execute("INSERT INTO dbo.Transfers (FromAccountID, ToAccountID, Amount, TransferDate) VALUES (?, ?, ?, GETDATE())",
                           (logged_user_id, recipient_id, amount))

            conn.commit()

            messagebox.showinfo("Succes", f"Transfer de {amount} realizat către utilizatorul {recipient_id}.")

            show_content("view_accounts", content_frame)

        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la procesarea transferului: {e}")
        except Exception as e:
            messagebox.showerror("Eroare", f"A apărut o eroare: {str(e)}")
        finally:
            conn.close()

def view_personal_data(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    ttk.Label(content_frame, text="Datele personale:", font=("Helvetica", 16, "bold")).pack(pady=10)

    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Username, PasswordHash, Role FROM dbo.Users WHERE ClientID = ?", (logged_user_id,))
            user_data = cursor.fetchone()

            if user_data:
                ttk.Label(content_frame, text=f"Username: {user_data[0]}", font=("Helvetica", 12)).pack(pady=5)
                ttk.Label(content_frame, text="Password: [Protejat]", font=("Helvetica", 12)).pack(pady=5)
                ttk.Label(content_frame, text=f"Role: {user_data[2]}", font=("Helvetica", 12)).pack(pady=5)
            else:
                messagebox.showinfo("Info", "Nu s-au găsit date personale.")
        except pyodbc.Error as e:
            messagebox.showerror("Eroare", f"Eroare la încărcarea datelor personale: {e}")
        finally:
            conn.close()

def user_interface():
    global show_content
    global logged_user_id

    root = tk.Tk()
    root.title("User Panel")
    root.geometry("900x600")
    root.configure(bg="#2C3E50") 

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 14, "bold"), background="#2C3E50", foreground="white")
    style.configure("TButton", font=("Arial", 11), padding=10)
    style.configure("TFrame", background="#34495E")

    title_label = ttk.Label(root, text="Interfața Utilizatorului", font=("Arial", 18, "bold"), anchor="center")
    title_label.pack(pady=15)

    sidebar = ttk.Frame(root, width=200, relief="ridge", padding=10)
    sidebar.pack(side=tk.LEFT, fill=tk.Y)

    buttons = [
        ("Vezi Loan", "loan"),
        ("Solicită Împrumut", "add_loan"),
        ("Vezi Date Personale", "personal_data"),
        ("Transferă Bani", "transfer"),
        #("Adaugă Fonduri", "add_funds"),
        ("Vezi Conturi", "view_accounts"),
        ("Ieși", "exit")
    ]

    for text, command in buttons:
        btn = ttk.Button(sidebar, text=text, style="TButton", command=lambda cmd=command: show_content(cmd, content_frame) if cmd != "exit" else root.quit())
        btn.pack(fill=tk.X, pady=5)

    content_frame = ttk.Frame(root, relief="ridge", padding=15)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    root.mainloop()

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

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x300")
login_window.configure(bg="#2C3E50") 

style = ttk.Style()
style.configure("TLabel", font=("Arial", 12, "bold"), background="#2C3E50", foreground="white")
style.configure("TButton", font=("Arial", 11), background="#1ABC9C", foreground="black", padding=5)
style.configure("TEntry", font=("Arial", 11), padding=5)

frame_login = tk.Frame(login_window, bg="#34495E", padx=20, pady=20)
frame_login.place(relx=0.5, rely=0.5, anchor="center")

ttk.Label(frame_login, text="Username:").grid(row=0, column=0, pady=5, sticky="w")
entry_username = ttk.Entry(frame_login, width=30)
entry_username.grid(row=0, column=1, pady=5)

ttk.Label(frame_login, text="Password:").grid(row=1, column=0, pady=5, sticky="w")
entry_password = ttk.Entry(frame_login, width=30, show="*")
entry_password.grid(row=1, column=1, pady=5)

btn_login = ttk.Button(frame_login, text="Login", command=check_login, style="TButton")
btn_login.grid(row=2, columnspan=2, pady=15)

login_window.mainloop()

login_window.mainloop()



