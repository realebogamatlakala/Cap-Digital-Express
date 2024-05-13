#imports
from tkinter import *
import os
from PIL import ImageTk, Image

#Main Screen
master = Tk()
master.title('Banking App')

#Functions
def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    all_accounts = os.listdir()

    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red",text="All fields requried * ")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red",text="Account already exists")
            return
        else:
            new_file = open(name,"w")
            new_file.write(name+'\n')
            new_file.write(password+'\n')
            new_file.write(age+'\n')
            new_file.write(gender+'\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text="Account has been created")

def register():
    #Vars
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()
    
    #Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')

    #Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(register_screen, text="Name", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(register_screen, text="Age", font=('Calibri',12)).grid(row=2,sticky=W)
    Label(register_screen, text="Gender", font=('Calibri',12)).grid(row=3,sticky=W)
    Label(register_screen, text="Password", font=('Calibri',12)).grid(row=4,sticky=W)
    notif = Label(register_screen, font=('Calibri',12))
    notif.grid(row=6,sticky=N,pady=10)

    #Entries
    Entry(register_screen,textvariable=temp_name).grid(row=1,column=0)
    Entry(register_screen,textvariable=temp_age).grid(row=2,column=0)
    Entry(register_screen,textvariable=temp_gender).grid(row=3,column=0)
    Entry(register_screen,textvariable=temp_password,show="*").grid(row=4,column=0)

    #Buttons
    Button(register_screen, text="Register", command = finish_reg, font=('Calibri',12)).grid(row=5,sticky=N,pady=10)

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
            #Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                #Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
                Label(account_dashboard, text="Welcome "+name, font=('Calibri',12)).grid(row=1,sticky=N,pady=5)
                #Buttons
                Button(account_dashboard, text="Personal Details",font=('Calibri',12),width=30,command=personal_details).grid(row=2,sticky=N,padx=10)
                Button(account_dashboard, text="Deposit",font=('Calibri',12),width=30,command=deposit).grid(row=3,sticky=N,padx=10)
                Button(account_dashboard, text="Withdraw",font=('Calibri',12),width=30,command=withdraw).grid(row=4,sticky=N,padx=10)
                Label(account_dashboard).grid(row=5,sticky=N,pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!!")
                return
    login_notif.config(fg="red", text="No account found !!")
def update_balance_label():
    global login_name, balance_label
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = float(user_details[4])
    balance_label.config(text=f"Balance: £{details_balance}")
    
def deposit():
    global login_name
    
    def finish_deposit():
        deposit_input = deposit_entry.get()
        if not deposit_input:
            deposit_notif.config(fg="red", text="Please enter a valid amount.")
            return
        try:
            deposit_amount = float(deposit_input)
            if deposit_amount <= 0:
                deposit_notif.config(fg="red", text="Invalid amount. Please enter a positive number.")
                return
        except ValueError:
            deposit_notif.config(fg="red", text="Invalid input. Please enter a valid number.")
            return
        
        # Proceed with the deposit operation
        file = open(login_name, 'r')
        file_data = file.read()
        user_details = file_data.split('\n')
        details_balance = float(user_details[4])
        new_balance = details_balance + deposit_amount
        file.close()
        file = open(login_name, 'w')
        file.write(user_details[0]+'\n')
        file.write(user_details[1]+'\n')
        file.write(user_details[2]+'\n')
        file.write(user_details[3]+'\n')
        file.write(str(new_balance))
        file.close()
        
        # Update BankData.txt with new balance
        with open("BankData.txt", "a") as bank_file:
            bank_file.write(f"{login_name}:{new_balance}\n")
        
        # Log transaction in TransactionLog.txt
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"Deposit: {deposit_amount}\n")
        
        deposit_notif.config(fg="green", text=(f"{login_name} Deposited {deposit_amount} successfully!!!\n New Balance: {new_balance}"))
    
    deposit_screen = Toplevel(master)
    deposit_screen.title("Deposit")
    
    Label(deposit_screen, text="How much would you like to deposit:").grid(row=0, column=0, padx=10, pady=5)
    deposit_entry = Entry(deposit_screen)
    deposit_entry.grid(row=0, column=1, padx=10, pady=5)
    deposit_button = Button(deposit_screen, text="Deposit", command=finish_deposit)
    deposit_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    deposit_notif = Label(deposit_screen, font=('Calibri',12))
    deposit_notif.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

def withdraw():
    global login_name
    
    def finish_withdrawal():
        withdrawal_input = withdrawal_entry.get()
        if not withdrawal_input:
            withdrawal_notif.config(fg="red", text="Please enter a valid amount.")
            return
        try:
            withdrawal_amount = float(withdrawal_input)
            if withdrawal_amount <= 0:
                withdrawal_notif.config(fg="red", text="Invalid amount. Please enter a positive number.")
                return
        except ValueError:
            withdrawal_notif.config(fg="red", text="Invalid input. Please enter a valid number.")
            return
        
        # Proceed with the withdrawal operation
        file = open(login_name, 'r')
        file_data = file.read()
        user_details = file_data.split('\n')
        details_balance = float(user_details[4])
        
        if withdrawal_amount > details_balance:
            withdrawal_notif.config(fg="red", text="Insufficient funds.")
            return
        
        new_balance = details_balance - withdrawal_amount
        file.close()
        
        # Update user's account file with the new balance
        file = open(login_name, 'w')
        file.write(user_details[0]+'\n')
        file.write(user_details[1]+'\n')
        file.write(user_details[2]+'\n')
        file.write(user_details[3]+'\n')
        file.write(str(new_balance))
        file.close()
        
        # Update BankData.txt with new balance
        with open("BankData.txt", "a") as bank_file:
            bank_file.write(f"{login_name}:{new_balance}\n")
        
        # Log transaction in TransactionLog.txt
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"Withdrawal: {withdrawal_amount}\n")
        
        withdrawal_notif.config(fg="green", text=(f"{login_name} withdrew {withdrawal_amount} successfully!!!\n New Balance: {new_balance}"))

    withdrawal_screen = Toplevel(master)
    withdrawal_screen.title("Withdrawal")
    
    Label(withdrawal_screen, text="How much would you like to 'withdraw':").grid(row=0, column=0, padx=10, pady=5)
    withdrawal_entry = Entry(withdrawal_screen)
    withdrawal_entry.grid(row=0, column=1, padx=10, pady=5)
    withdrawal_button = Button(withdrawal_screen, text="Withdraw", command=finish_withdrawal)
    withdrawal_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
    withdrawal_notif = Label(withdrawal_screen, font=('Calibri',12))
    withdrawal_notif.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    
def personal_details():
    #Vars
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]
    #Personal details screen
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')
    #Labels
    Label(personal_details_screen, text="Personal Details", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(personal_details_screen, text="Name : "+details_name, font=('Calibri',12)).grid(row=1,sticky=W)
    Label(personal_details_screen, text="Age : "+details_age, font=('Calibri',12)).grid(row=2,sticky=W)
    Label(personal_details_screen, text="Gender : "+details_gender, font=('Calibri',12)).grid(row=3,sticky=W)
    Label(personal_details_screen, text="Balance :£"+details_balance, font=('Calibri',12)).grid(row=4,sticky=W)
def login():
    #Vars
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()
    #Login Screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    #Labels
    Label(login_screen, text="Login to your account", font=('Calibri',12)).grid(row=0,sticky=N,pady=10)
    Label(login_screen, text="Username", font=('Calibri',12)).grid(row=1,sticky=W)
    Label(login_screen, text="Password", font=('Calibri',12)).grid(row=2,sticky=W)
    login_notif = Label(login_screen, font=('Calibri',12))
    login_notif.grid(row=4,sticky=N)
    #Entry
    Entry(login_screen, textvariable=temp_login_name).grid(row=1,column=1,padx=5)
    Entry(login_screen, textvariable=temp_login_password,show="*").grid(row=2,column=1,padx=5)
    #Button
    Button(login_screen, text="Login", command=login_session, width=15,font=('Calibri',12)).grid(row=3,sticky=W,pady=5,padx=5)

#Image import
img = Image.open('secure.png')
img = img.resize((150,150))
img = ImageTk.PhotoImage(img)

#Labels
Label(master, text = "Cap-Digital-Express", font=('Calibri',14)).grid(row=0,sticky=N,pady=10)
Label(master, text = "Bank Better with CDE Bank! \n The most secure bank in the southern hemisphere!", font=('Calibri',12)).grid(row=1,sticky=N)
Label(master, image=img).grid(row=2,sticky=N,pady=15)

#Buttons
Button(master, text="Register", font=('Calibri',12),width=20,command=register).grid(row=3,sticky=N)
Button(master, text="Login", font=('Calibri',12),width=20,command=login).grid(row=4,sticky=N,pady=10)

master.mainloop()
