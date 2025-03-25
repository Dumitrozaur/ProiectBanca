import pyodbc

def getDBConnection():
    SERVER_NAME = "DESKTOP-AS1QGLB"
    DATABASE_NAME = "BankDB"
    CONN_STRING = f"DRIVER={{SQL Server}};SERVER={SERVER_NAME};DATABASE={DATABASE_NAME};Trusted_Connection=yes;"

    try:
        conn = pyodbc.connect(CONN_STRING)
        return conn
    except pyodbc.Error as e:
        print(f"Database connection error: {e}")
        return None

##############################################
###TABELA CLIENT PLUS TABELELE CE CONTIN FK###
##############################################

    # dataClient = (
    #     casuta_nume,                 
    #     casute_prenume,                  
    #     casuta_data_nasterii,           
    #     casuta_email, 
    #     casuta_telefon,         
    #     casuta_adresa        
    # )

    # dataBills = (
    #     casuta_client_id,
    #     casuta_suma,
    #     casuta_data_emitere,
    #     casuta_data_status
    # )

    # dataUsers = (
    #     casuta_client_id,
    #     casuta_username,
    #     casuta_password,
    #     casuta_role
    # )

    # dataLoginSessions = (
    #     casuta_user_id,
    #     casuta_login_date,
    #     casuta_logout_date
    # )

    # dataAuditLogs = (
    #     casuta_user_id,
    #     casuta_action,
    #     casuta_date
    # )

    # dataDeposits = (
    #     casuta_client_id,
    #     casuta_suma,
    #     casuta_data,
    #     casuta_IterestRate
    # )

    # dataCreditCards = (
    #     casuta_client_id,
    #     casuta_card_number,
    #     casuta_expiration_date,
    #     casuta_cvv,
    #     casuta_credit_limit
    # )

    # dataLoans = (
    #     casuta_client_id,
    #     casuta_suma,
    #     casuta_interes_rate,
    #     casuta_data_start,
    #     casuta_data_end,
    #     casuta_status
    # )

    # dataLoanPayments = (
    #     casuta_loan_id,
    #     casuta_suma,
    #     casuta_data_plata
    # )

    # dataAccounts = (
    #     casuta_client_id,
    #     casuta_tipul_contului,
    #     casuta_balanta,
    #     casuta_data_deschiderii,
    #     casuta_data_inchiderii,
    #     casuta_status
    # )

    # dataTransfer = (
    #     casuta_account_id,
    #     casuta_suma,
    #     casuta_data_transfer,
    #     casuta_account_id_destinatie
    # )

    # dataTransaction = (
    #     casuta_account_id,
    #     casuta_suma,
    #     casuta_data_tranzactie,
    #     casuta_tipul_tranzactiei
    # )

###############################################
###TABELA ANGAJAT PLUS TABELELE CE CONTIN FK###
###############################################

    # dataAngajati = (
    #     casuta_nume,
    #     casute_prenume,
    #     casuta_pozitie,
    #     casuta_data_angajare,
    #     casuta_salariu,
    #     casuta_email
    # )

############################################
###TABELA Branch PLUS TABELELE CE CONTIN FK###
############################################

    # dataBranch = (
    #     casuta_nume,
    #     casuta_locatie
    # )

    # dataATM = (
    #     casuta_branch_id,
    #     casuta_locatie
    # )

############################################
############################################
############################################
