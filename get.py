import pyodbc
from gestiune import *

def get_clients():
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ClientID, FirstName, LastName, DOB, Email, PhoneNumber, Address FROM dbo.Clients")
        clients = cursor.fetchall()
        conn.close()
        return clients
    return []

def get_bills(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT BillID, {clientID}, Amount, DueDate, Status FROM dbo.Bills")
        bills = cursor.fetchall()
        conn.close()
        return bills
    return []

def get_users(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT UserID, {clientID}, Username, PasswordHash, Role FROM dbo.Users")
        users = cursor.fetchall()
        conn.close()
        return users
    return []

def get_login_sessions(userID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT SessionID, {userID}, LoginTime, LogoutTime FROM dbo.LoginSessions")
        login_sessions = cursor.fetchall()
        conn.close()
        return login_sessions
    return []

def get_audit_logs(userID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT LogID, {userID}, Action, Timestamp FROM dbo.AuditLogs")
        audit_logs = cursor.fetchall()
        conn.close()
        return audit_logs
    return []

def get_deposits(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT DepositID, {clientID}, Amount, InterestRate, MaturityDate FROM dbo.Deposits")
        deposits = cursor.fetchall()
        conn.close()
        return deposits
    return []

def get_credit_cards(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT CardID, {clientID}, CardNumber, ExpiryDate, CVV, CreditLimit FROM dbo.CreditCards")
        credit_cards = cursor.fetchall()
        conn.close()
        return credit_cards
    return []

def get_loans(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT LoanID, {clientID}, Amount, InterestRate, StartDate, EndDate, Status FROM dbo.Loans")
        loans = cursor.fetchall()
        conn.close()
        return loans
    return []

def get_loan_payments(loanID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT PaymentID, {loanID}, AmountPaid, PaymentDate FROM dbo.LoanPayments")
        loan_payments = cursor.fetchall()
        conn.close()
        return loan_payments
    return []

def get_accounts(clientID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT AccountID, {clientID}, AccountType, Balance, OpenDate, Status FROM dbo.Accounts")
        accounts = cursor.fetchall()
        conn.close()
        return accounts
    return []

def get_transfer(fromAccountID, toAccountID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT TransferID, {fromAccountID}, {toAccountID}, Amount, TransferDate FROM dbo.Transfers")
        transfers = cursor.fetchall()
        conn.close()
        return transfers
    return []

def get_transaction(acountID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT TransactionID, {acountID}, TransactionType, Amount, TransactionDate FROM dbo.Transactions")
        transactions = cursor.fetchall()
        conn.close()
        return transactions
    return []

def get_employees():
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT EmployeeID, FirstName, LastName, Position, HireDate, Salary, Email FROM dbo.Employees")
        employees = cursor.fetchall()
        conn.close()
        return employees
    return []

def get_branch():
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT BranchID, BranchName, Location FROM dbo.Branches")
        branch = cursor.fetchall()
        conn.close()
        return branch
    return []
    
def get_atm(branchID):
    conn = getDBConnection()
    if conn:
        cursor = conn.cursor
        cursor.execute(f"SELECT ATMID, {branchID}, Location FROM dbo.ATMs")
        atm = cursor.fetchall()
        conn.close()
        return atm
    return []