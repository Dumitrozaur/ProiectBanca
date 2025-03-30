import pyodbc
from gestiune import *

def insert_client(casuta_nume, casute_prenume, casuta_data_nasterii, casuta_email, casuta_telefon, casuta_adresa):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Clients (FirstName, LastName, DOB, Email, PhoneNumber, Address) 
            OUTPUT INSERTED.ClientID VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, casuta_nume, casute_prenume, casuta_data_nasterii, casuta_email, casuta_telefon, casuta_adresa)
            client_id = cursor.fetchone()[0]
            conn.commit()
            print(f"Client adaugat cu succes cu ID: {client_id}")
            return client_id
        except pyodbc.Error as e:
            print(f"Inserting Client error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_bill(casuta_client_id, casuta_suma, casuta_data_emitere, casuta_data_status):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Bills (ClientID, Amount, DueDate, Status)
            OUTPUT INSERTED.BillID 
            VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_suma, casuta_data_emitere, casuta_data_status)
            conn.commit()
            print(f"Bill adaugat cu succes pentru clientul cu ID: {casuta_client_id}")
        except pyodbc.Error as e:
            print(f"Inserting Bill error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_user(casuta_client_id, casuta_username, casuta_password, casuta_role):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Users (ClientID, Username, PasswordHash, Role)
            OUTPUT INSERTED.UserID
            VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_username, casuta_password, casuta_role)
            user_id = cursor.fetchone()[0]
            conn.commit()
            print(f"{casuta_username} adaugat cu succes cu ID: {user_id}")
            return user_id
        except pyodbc.Error as e:
            print(f"Inserting User error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_login_session(casuta_user_id, casuta_login_date, casuta_logout_date):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.LoginSessions (UserID, LoginTime, LogoutTime)
            VALUES (?, ?, ?)"""
            cursor.execute(sql, casuta_user_id, casuta_login_date, casuta_logout_date)
            conn.commit()
            print(f"Login session adaugat cu succes pentru userul cu ID: {casuta_user_id}")
        except pyodbc.Error as e:
            print(f"Inserting Login Session error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_audit_log(casuta_user_id, casuta_action, casuta_date):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.AuditLogs (UserID, Action, Timestamp)
            VALUES (?, ?, ?)"""
            cursor.execute(sql, casuta_user_id, casuta_action, casuta_date)
            conn.commit()
            print(f"Audit log adaugat cu succes pentru userul cu ID: {casuta_user_id}")
        except pyodbc.Error as e:
            print(f"Inserting Audit Log error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_deposit(casuta_client_id, casuta_suma, casuta_data, casuta_Interest_Rate):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Deposits (ClientID, Amount, InterestRate, MaturityDate)
            VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_suma, casuta_Interest_Rate, casuta_data)
            conn.commit()
            print(f"Depozit adaugat cu succes pentru clientul cu ID: {casuta_client_id}")
        except pyodbc.Error as e:
            print(f"Inserting Deposit error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_credit_card(casuta_client_id, casuta_card_number, casuta_expiration_date, casuta_cvv, casuta_credit_limit):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.CreditCards (ClientID, CardNumber, ExpiryDate, CVV, CreditLimit) VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_card_number, casuta_expiration_date, casuta_cvv, casuta_credit_limit)
            conn.commit()
            print(f"Card adaugat cu succes pentru clientul cu ID: {casuta_client_id}")
        except pyodbc.Error as e:
            print(f"Inserting Credit Card error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_loans(casuta_client_id, casuta_suma, casuta_interes_rate, casuta_data_start, casuta_data_end, casuta_status):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Loans (ClientID, Amount, InterestRate, StartDate, EndDate, Status) VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_suma, casuta_interes_rate, casuta_data_start, casuta_data_end, casuta_status)
            conn.commit()
            print(f"Credit adaugat cu succes pentru clientul cu ID: {casuta_client_id}")
        except pyodbc.Error as e:
            print(f"Inserting Loan error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_loan_payment(casuta_loan_id, casuta_suma, casuta_data_plata):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.LoanPayments (LoanID, AmountPaid, PaymentDate) VALUES (?, ?, ?)"""
            cursor.execute(sql, casuta_loan_id, casuta_suma, casuta_data_plata)
            conn.commit()
            print(f"Plata credit adaugata cu succes pentru creditul cu ID: {casuta_loan_id}")
        except pyodbc.Error as e:
            print(f"Inserting Loan Payment error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_account(casuta_client_id, casuta_tpul_contului, casuta_balanta, casuta_data_deschiderii, casuta_status):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Accounts (ClientID, AccountType, Balance, OpenDate, Status) VALUES (?, ?, ?, ?, ?)"""
            cursor.execute(sql, casuta_client_id, casuta_tpul_contului, casuta_balanta, casuta_data_deschiderii, casuta_status)
            conn.commit()
            print(f"Cont adaugat cu succes pentru clientul cu ID: {casuta_client_id}")
        except pyodbc.Error as e:
            print(f"Inserting Account error: {e}")
        finally:
            cursor.close()
            conn.close()
#trebe sa fac debug aici!!
def insert_transfer(casuta_account_id, casuta_account_id_destinatie, casuta_suma, casuta_data_transfer):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Transfers (FromAccountID, ToAccountID, Amount, TransferDate) VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, casuta_account_id, casuta_account_id_destinatie, casuta_suma, casuta_data_transfer)
            conn.commit()
            print(f"Transfer adaugat cu succes pentru contul cu ID: {casuta_account_id}")
        except pyodbc.Error as e:
            print(f"Inserting Transfer error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_trasaction(casuta_account_id, casuta_tip_tranzactie, casuta_suma, casuta_data_tranzactie):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Transactions (AccountID, TransactionType, Amount, TransactionDate,) VALUES (?, ?, ?, ?)"""
            cursor.execute(sql, casuta_account_id, casuta_tip_tranzactie, casuta_suma, casuta_data_tranzactie)
            conn.commit()
            print(f"Tranzactie adaugata cu succes pentru contul cu ID: {casuta_account_id}")
        except pyodbc.Error as e:
            print(f"Inserting Transaction error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_angajati(casuta_nume, casuta_prenume, casuta_functie, casuta_data_angajarii, casuta_salariu, casuta_email):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Employees (FirstName, LastName, Position, HireDate, Salary, Email) VALUES (?, ?, ?, ?, ?, ?)"""
            cursor.execute(sql, casuta_nume, casuta_prenume, casuta_functie, casuta_data_angajarii, casuta_salariu, casuta_email)
            conn.commit()
            print(f"Angajat adaugat cu succes cu functia: {casuta_functie}")
        except pyodbc.Error as e:
            print(f"Inserting Employee error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_departament(casuta_nume_departament, casuta_locatie):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.Branches (BranchName, Location) VALUES (?, ?)"""
            cursor.execute(sql, casuta_nume_departament, casuta_locatie)
            conn.commit()
            print(f"Departament adaugat cu succes cu numele: {casuta_nume_departament}")
        except pyodbc.Error as e:
            print(f"Inserting Department error: {e}")
        finally:
            cursor.close()
            conn.close()

def insert_ATM(casuta_branch_id, casuta_locatie):
    conn = getDBConnection()
    if conn:
        try:
            cursor = conn.cursor()
            sql = """INSERT INTO dbo.ATMs (BranchID, Location) VALUES (?, ?)"""
            cursor.execute(sql, casuta_branch_id, casuta_locatie)
            conn.commit()
            print(f"ATM adaugat cu succes cu locatia: {casuta_locatie}")
        except pyodbc.Error as e:
            print(f"Inserting ATM error: {e}")
        finally:
            cursor.close()
            conn.close()

insert_client("Valentrin", "Ciprian", "2000-10-10", "cipri@gmail.com", "0740123456", "Str. Florilor, nr. 1")
insert_user(4, "Cipri", "1234", "Employee")
