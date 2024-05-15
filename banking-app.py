# import os
# from tkinter import *
# from tkinter import messagebox, filedialog
# from PIL import Image, ImageTk

# master = Tk()
# master.title('Banking App')

# # Functions
# def finish_reg():
#     name = temp_name.get()
#     age = temp_age.get()
#     gender = temp_gender.get()
#     account = temp_accountNo()
#     password = temp_password.get()
#     all_accounts = os.listdir()

#     if name == "" or age == "" or gender == "" or account == ""or password == "":
#         notif.config(fg="red",text="All fields required * ")
#         return

#     for name_check in all_accounts:
#         if name == name_check:
#             notif.config(fg="red",text="Account already exists")
#             return
#         else:
#             new_file = open(name,"w")
#             new_file.write(name+'\n')
#             new_file.write(password+'\n')
#             new_file.write(age+'\n')
#             new_file.write(gender+'\n')
#             new_file.write(account + '\n')
#             new_file.write('0')
#             new_file.close()
#             notif.config(fg="green", text="Account has been created")

# def register():
#     #Vars
#     global temp_name, temp_age, temp_gender,temp_accountNo, temp_password, notif

#     temp_name = StringVar()
#     temp_age = StringVar()
#     temp_gender = StringVar()
#     temp_accountNo = StringVar()
#     temp_password = StringVar()
    
#     # Register Screen
#     register_screen = Toplevel(master)
#     register_screen.title('Register')

#     # Labels
#     Label(register_screen, text="Please enter your details below to register", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
#     Label(register_screen, text="Name", font=('Calibri',12)).grid(row=1,sticky=W)
#     Label(register_screen, text="Age", font=('Calibri',12)).grid(row=2,sticky=W)
#     Label(register_screen, text="Gender", font=('Calibri',12)).grid(row=3,sticky=W)
#     Label(register_screen,text="Account No:", font=('Calibri',12)).grid(row=4,sticky=W)
#     Label(register_screen, text="Password", font=('Calibri',12)).grid(row=5,sticky=W)
#     notif = Label(register_screen, font=('Calibri',12))
#     notif.grid(row=6,sticky=N,pady=10)

#     # Entries
#     Entry(register_screen, textvariable=temp_name).grid(row=1,column=0)
#     Entry(register_screen, textvariable=temp_age).grid(row=2,column=0)
#     Entry(register_screen, textvariable=temp_gender).grid(row=3,column=0)
#     Entry(register_screen, textvariable=temp_accountNo).grid(row=4,column=0)
#     Entry(register_screen, textvariable=temp_password,show="*").grid(row=5,column=0)

#     # Buttons
#     Button(register_screen, text="Register", command = finish_reg, font=('Calibri',12)).grid(row=6,sticky=N,pady=10)
import os
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import string

master = Tk()
master.title('Banking App')

# Functions
def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    account = generate_account_number()
    password = generate_password()
    all_accounts = os.listdir()

    if name == "" or age == "" or gender == "":
        notif.config(fg="red", text="All fields required * ")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red", text="Account already exists")
            return
        else:
            new_file = open(name + ".txt", "w")
            new_file.write(name + '\n')
            new_file.write(password + '\n')
            new_file.write(age + '\n')
            new_file.write(gender + '\n')
            new_file.write(account + '\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text="Account has been created")

            # Display generated account number and password
            temp_accountNo.set(account)
            temp_password.set(password)

def generate_account_number():
    # Generate a random 8-digit account number
    return ''.join(random.choices(string.digits, k=8))

def generate_password():
    # Generate a random password with 12 characters
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*()'

    password_characters = uppercase_letters + lowercase_letters + digits + special_characters
    return ''.join(random.choices(password_characters, k=12))

def register():
    # Vars
    global temp_name, temp_age, temp_gender, temp_accountNo, temp_password, notif

    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_accountNo = StringVar()
    temp_password = StringVar()

    # Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Name", font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W)
    Label(register_screen, text="Gender", font=('Calibri', 12)).grid(row=3, sticky=W)
    Label(register_screen, text="Account No", font=('Calibri', 12)).grid(row=4, sticky=W)
    Label(register_screen, text="Password", font=('Calibri', 12)).grid(row=5, sticky=W)
    notif = Label(register_screen, font=('Calibri', 12))
    notif.grid(row=6, sticky=N, pady=10)

    # Entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0, padx=20)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0, padx=20)
    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0, padx=20)
    Entry(register_screen, textvariable=temp_accountNo).grid(row=4, column=0, padx=20)
    Entry(register_screen, textvariable=temp_password, show="*").grid(row=5, column=0, padx=20)

    # Buttons
    Button(register_screen, text="Register", command=finish_reg, font=('Calibri', 12)).grid(row=6, columnspan=2, sticky=N, pady=10)


def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name,"r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password  = file_data[1]
            # Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                # Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri',12)).grid(row=0,sticky=N,pady=10, padx=150) 
                Label(account_dashboard, text="Welcome " +name+ "\n \n Would you like to make a transaction?", font=('Calibri',12)).grid(row=1,sticky=N,pady=5, padx=150)
                # Buttons
                Button(account_dashboard, text="Yes",width=20, command=transaction_screen, font=('Calibri',12)).grid(row=2,sticky=N,pady=5)
                Button(account_dashboard, text="No",width=20, command=account_dashboard.destroy, font=('Calibri',12)).grid(row=3,sticky=N,pady=5)
                # Buttons
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!!")
                return
    login_notif.config(fg="red", text="No account found!!!")

def view_transactions(username):
    try:
        with open(username, "r") as file:
            user_data = file.readlines()
            balance = user_data[-1].strip()  # Get balance from the last line
        transactions = []  # Initialize an empty list to store transactions
        with open("TransactionLog.txt", "r") as file:
            for line in file:
                if line.startswith(username):
                    transactions.append(line.strip())  # Append transactions of the user
    except FileNotFoundError:
        messagebox.showerror("Error", "Transaction log file not found.")
        return

    # Create a new window for displaying transactions
    transactions_window = Toplevel(master)
    transactions_window.title('Transactions History')

    # Display user's details and balance
    Label(transactions_window, text=f"Username: {username}", font=('Calibri', 12)).grid(row=0, columnspan=2, sticky=W, padx=10, pady=5)
    Label(transactions_window, text=f"Balance: R{balance}", font=('Calibri', 12)).grid(row=1, columnspan=2, sticky=W, padx=10, pady=5)

    # Display transactions in a scrollable text widget
    scrollbar = Scrollbar(transactions_window)
    scrollbar.grid(row=2, column=1, sticky=NS)
    text = Text(transactions_window, wrap=WORD, yscrollcommand=scrollbar.set, font=('Calibri', 12))
    text.grid(row=2, column=0, sticky=NSEW, padx=10, pady=5)
    
    for transaction in transactions:
        text.insert(END, transaction + "\n")

    # Set scrollbar to scroll text widget
    scrollbar.config(command=text.yview)

    # Create a button to download transaction history
    Button(transactions_window, text="Download Transaction History", font=('Calibri', 12), command=lambda: download_transactions(username, transactions)).grid(row=3, columnspan=2, pady=10)

def download_transactions(username, transactions):
    download_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if download_location:
        with open(download_location, "w") as file:
            file.writelines(transactions)
        messagebox.showinfo("Success", "Transaction history downloaded successfully.")

def transaction_screen():
    # Create a new Toplevel window for the transaction screen
    transaction_screen = Toplevel(master)
    transaction_screen.title('Transactions')

    # Labels
    Label(transaction_screen, text="Transaction Menu", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10, padx=150)
    Label(transaction_screen, text="Please select an option:", font=('Calibri', 12)).grid(row=1, sticky=N, pady=5, padx=150)

    # Buttons
    Button(transaction_screen, text="Personal Details", font=('Calibri', 12), width=30, command=personal_details).grid(row=2, sticky=N, padx=150)
    Button(transaction_screen, text="Deposit", font=('Calibri', 12), width=30, command=deposit).grid(row=3, sticky=N, padx=150)
    Button(transaction_screen, text="Withdraw", font=('Calibri', 12), width=30, command=withdraw).grid(row=4, sticky=N, padx=150)
    Button(transaction_screen, text="View Transactions", font=('Calibri', 12), command=lambda: view_transactions(login_name)).grid(row=5, pady=10)

def personal_details():
    # Vars
    file = open(login_name, 'r')
    user_details = file.readlines()
    file.close()
    details_name = user_details[0].strip()
    details_age = user_details[2].strip()
    details_gender = user_details[3].strip()
    details_balance = user_details[-1].strip()

    # Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')

    # Labels
    Label(personal_details_screen, text="Personal Details", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen, text="Name : "+details_name, font=('Calibri',12)).grid(row=1,sticky=W)
    Label(personal_details_screen, text="Age : "+details_age, font=('Calibri',12)).grid(row=2,sticky=W)
    Label(personal_details_screen, text="Gender : "+details_gender, font=('Calibri',12)).grid(row=3,sticky=W)
    Label(personal_details_screen, text="Balance :R"+details_balance, font=('Calibri',12)).grid(row=4,sticky=W)
    Label(personal_details_screen, text="Balance :R"+details_balance, font=('Calibri',12)).grid(row=4,sticky=W)

def deposit():
    # Function to handle deposit
    def finish_deposit():
        deposit_input = deposit_entry.get()
        if not deposit_input:
            deposit_notif.config(fg="red", text="Please enter an amount.")
            return
        try:
            deposit_amount = float(deposit_input)
            if deposit_amount <= 0:
                deposit_notif.config(fg="red", text="Invalid amount. Please enter a positive amount.")
                return
        except ValueError:
            deposit_notif.config(fg="red", text="Invalid input. Please enter a valid amount.")
            return
        
        # Proceed with the deposit operation
        file = open(login_name, 'r+')
        user_data = file.readlines()
        balance = float(user_data[-1])  # Get balance from the last line
        new_balance = balance + deposit_amount
        
        # Update balance in user's file
        user_data[-1] = str(new_balance) + '\n'
        file.seek(0)
        file.writelines(user_data)
        file.close()
        
        # Log deposit transaction
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"{login_name}: Deposit: {deposit_amount}\n")
        
        deposit_notif.config(fg="green", text=(f"Deposit successful. New Balance: R{new_balance}"))

    deposit_screen = Toplevel(master)
    deposit_screen.title("Deposit")
    
    # Labels and Entry
    Label(deposit_screen, text="How much would you like to deposit:").grid(row=0, column=0, padx=10, pady=5)
    deposit_entry = Entry(deposit_screen)
    deposit_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Button and Notification Label
    Button(deposit_screen, text="Deposit", command=finish_deposit).grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    deposit_notif = Label(deposit_screen, font=('Calibri',12))
    deposit_notif.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

def withdraw():
    # Function to handle withdrawal
    def finish_withdrawal():
        withdrawal_input = withdrawal_entry.get()
        if not withdrawal_input:
            withdrawal_notif.config(fg="red", text="Please enter an amount.")
            return
        try:
            withdrawal_amount = float(withdrawal_input)
            if withdrawal_amount <= 0:
                withdrawal_notif.config(fg="red", text="Invalid amount. Please enter a positive amount.")
                return
        except ValueError:
            withdrawal_notif.config(fg="red", text="Invalid input. Please enter a valid amount.")
            return
        
        # Proceed with the withdrawal operation
        file = open(login_name, 'r+')
        user_data = file.readlines()
        balance = float(user_data[-1])  # Get balance from the last line
        
        if withdrawal_amount > balance:
            withdrawal_notif.config(fg="red", text="Insufficient funds.")
            file.close()
            return
        
        new_balance = balance - withdrawal_amount
        
        # Update balance in user's file
        user_data[-1] = str(new_balance) + '\n'
        file.seek(0)
        file.writelines(user_data)
        file.close()
        
        # Log withdrawal transaction
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"{login_name}: Withdrawal: {withdrawal_amount}\n")
        
        withdrawal_notif.config(fg="green", text=(f"Withdrawal successful. New Balance: R{new_balance}"))

    withdrawal_screen = Toplevel(master)
    withdrawal_screen.title("Withdrawal")
    
    # Labels and Entry
    Label(withdrawal_screen, text="How much would you like to withdraw:").grid(row=0, column=0, padx=10, pady=5)
    withdrawal_entry = Entry(withdrawal_screen)
    withdrawal_entry.grid(row=0, column=1, padx=10, pady=5)
    
    # Button and Notification Label
    Button(withdrawal_screen, text="Withdraw", command=finish_withdrawal).grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    withdrawal_notif = Label(withdrawal_screen, font=('Calibri',12))
    withdrawal_notif.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

def login():
    global temp_login_name, temp_login_password, login_notif, login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()

    login_screen = Toplevel(master)
    login_screen.title('Login')

    Label(login_screen, text="Login to your account", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Username", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(login_screen, text="Password", font=('Calibri',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen, font=('Calibri',12))
    login_notif.grid(row=4,sticky=N)

    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)

    Button(login_screen, text="Login", command=login_session, width=15,font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)

# Image import
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text = "Cap-Digital-Express", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "Bank Better with CDE Bank! \n The most secure bank in the southern hemisphere!", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2,sticky=N,pady=15)

Label(master, text = "If new user Register/ If Registered Login", font=('Calibri',12)).grid(row=3,sticky=N)
# Buttons
Button(master, text="Register", font=('Calibri',12),width=20,command=register).grid(row=4,sticky=N)
Button(master, text="Login", font=('Calibri',12),width=20,command=login).grid(row=5,sticky=N,pady=10)

master.mainloop()
