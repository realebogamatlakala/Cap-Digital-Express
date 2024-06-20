import os
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import random
import string
import requests
import pywhatkit
import shutil

# Function to send SMS notification
def send_sms_notification(recipient_number, message_text):
    url = "http://127.0.0.1:5000/send-sms"
    payload = {
        "to": recipient_number,
        "message": message_text
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Function to generate a random 8-digit account number
def generate_account_number():
    return ''.join(random.choices(string.digits, k=8))

# Function to generate a random password with 12 characters
def generate_password():
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    digits = string.digits
    special_characters = '!@#$%^&*()'

    password_characters = uppercase_letters + lowercase_letters + digits + special_characters
    return ''.join(random.choices(password_characters, k=12))

master = Tk()
master.title('Banking App')
master.configure(bg='DeepSkyBlue4')

def validate_cellphone(cellphone):
    # Check if the cellphone number starts with '0' and has a maximum length of 10 digits
    if len(cellphone) != 10 or not cellphone.startswith('0') or not cellphone.isdigit():
        return False
    return True

def finish_reg():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    cellphone = temp_cellphone.get()
    image = image_entry.get()

    # Generate random account number and password
    account = generate_account_number()
    password = generate_password()

    # Check if age is below 16
    try:
        if int(age) < 16:
            notif.config(fg="red", text="Minimum age is 16 years of age")
            return
    except ValueError:
        notif.config(fg="red", text="Invalid age entered")
        return

    if name == "" or age == "" or gender == "" or password == "" or image == "" or cellphone =="":
        notif.config(fg="red", text="All fields required *")
        return
    
    # Validate cellphone number
    if not validate_cellphone(cellphone):
        notif.config(fg="red", padx=10, text="Invalid cellphone number. Number should start with 0 with max 10 digits long.")
        return

    all_accounts = os.listdir()
    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red", text="Account already exists")
            return
    else:
        new_file = open(name, "w")
        new_file.write(name + '\n')
        new_file.write(password + '\n')
        new_file.write(age + '\n')
        new_file.write(gender + '\n')
        new_file.write(cellphone + '\n')
        new_file.write(account + '\n')
        new_file.write(image + '\n')
        new_file.write('0')
        new_file.close()
        notif.config(fg="green", text="Account has been created")
        # Display generated account number and password
        account_entry.delete(0, END)
        account_entry.insert(0, account)
        password_entry.delete(0, END)
        password_entry.insert(0, password)

# Rest of the code remains unchanged



def check_age(*args):
    try:
        age = int(temp_age.get())
        if age < 16:
            age_notif.config(fg="red", text="Minimum age is 16 years of age")
        else:
            age_notif.config(text="")
    except ValueError:
        age_notif.config(text="")

        # Optionally, send a welcome SMS
        sms_response = send_sms_notification(cellphone, f"Welcome to Transact Bank {name}, your account has been created.")
        if sms_response.get('success'):
            print("SMS sent successfully")
        else:
            print("Failed to send SMS", sms_response.get('error'))

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
    global temp_name, temp_age, temp_gender, temp_cellphone, temp_password, notif, account_entry, password_entry, image_entry

    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_cellphone = StringVar()
    temp_password = StringVar()

    # Register Screen
    register_screen = Toplevel(master)
    register_screen.title('Register')
    register_screen.configure(bg='DeepSkyBlue4')

    # Labels
    Label(register_screen, text="Please enter your details below to register", font=('Calibri', 12, 'bold')).grid(row=0, sticky=N, pady=5, padx=40)
    Label(register_screen, text="Username", font=('Calibri', 12),).grid(row=1, sticky=W, pady=2, padx=20)
    Label(register_screen, text="Age", font=('Calibri', 12)).grid(row=2, sticky=W, pady=2, padx=20)
    Label(register_screen, text="Gender", font=('Calibri', 12)).grid(row=3, sticky=W, pady=2, padx=20)
    Label(register_screen, text="Cellphone", font =('Calibri', 12)).grid(row=4,sticky=W, pady=2, padx=20)
    Label(register_screen, text="Account No", font=('Calibri', 12)).grid(row=5, sticky=W, pady=2, padx=20)
    Label(register_screen, text="Password", font=('Calibri', 12)).grid(row=6, sticky=W, pady=2, padx=20)
    notif = Label(register_screen, font=('Calibri', 12))
    notif.grid(row=7, sticky=N, pady=10)

    # Entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0, padx=30)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0, padx=30)
    
    # Bind age entry to check_age function
    temp_age.trace("w", check_age)
    
     # Gender dropdown
    temp_gender.set("Select")  # Default value
    gender_options = ["Male", "Female", "Other"]
    gender_menu = OptionMenu(register_screen, temp_gender, *gender_options)
    gender_menu.grid(row=3, column=1, padx=5)
    
    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0, padx=30)
    Entry(register_screen, textvariable=temp_cellphone).grid(row=4, column=0, padx=30)
    account_entry = Entry(register_screen)
    account_entry.grid(row=5, column=0, padx=30)
    password_entry = Entry(register_screen, textvariable=temp_password, show="")
    password_entry.grid(row=6, column=0, padx=30)

    # Image upload entry and button
    image_entry = Entry(register_screen)  # Initialize the image entry variable
    image_entry.grid(row=8, column=0, padx=30, pady=5)
    upload_button = Button(register_screen, text="Upload Image", command=upload_image, font=('Calibri', 10))
    upload_button.grid(row=8, column=1, padx=30, pady=5)

    # Register button
    Button(register_screen, text="Register", command=finish_reg, font=('Calibri', 12, 'bold'), width=15).grid(row=9, columnspan=1, sticky=N, pady=10)

def upload_image():
    global image_entry
    image_path = filedialog.askopenfilename()  # Open file dialog to select image
    image_entry.delete(0, END)  # Clear the entry field
    image_entry.insert(0, image_path)  # Insert the selected image path into the entry field

def login_session():
    global login_name, login_notif
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    # Ensure login_notif is defined at the correct place
    login_notif = Label(login_screen, font=('Calibri', 12, 'bold'), bg='DeepSkyBlue4') # Define the login_notif variable
    login_notif.grid(row=5, columnspan=2, pady=10)  # Place the label in the grid

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[1]
            cellphone = file_data[4]
            # Account Dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title('Dashboard')
                account_dashboard.configure(bg='DeepSkyBlue4')
                # Labels
                Label(account_dashboard, text="Account Dashboard", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10, padx=150) 
                Label(account_dashboard, text=f"Welcome {name}\n\nWould you like to make a transaction?", font=('Calibri', 12, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=2, sticky=N, pady=5, padx=150)
                # Display user image
                user_image_path = file_data[6]  # Image path is stored in the 7th line
                if os.path.exists(user_image_path):
                    user_image = Image.open(user_image_path)
                    user_image = user_image.resize((150, 150))
                    user_image = ImageTk.PhotoImage(user_image)
                    Label(account_dashboard, image=user_image, bg='DeepSkyBlue4').grid(row=1, sticky=N, pady=5)
                
                    account_dashboard.image = user_image
                # Buttons
                Button(account_dashboard, text="Yes", width=20, command=transaction_screen, font=('Calibri', 12, 'bold'), fg='white', bg='RoyalBlue3').grid(row=3, column=0, sticky=E, pady=5, padx=150)
                Button(account_dashboard, text="No", width=20, command=account_dashboard.destroy, font=('Calibri', 12, 'bold'), fg='white', bg='RoyalBlue3').grid(row=3, column=0, sticky=W, pady=5, padx=150)
                send_sms_notification(cellphone, f"Login successful for {name}.")
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!")
                return
    login_notif.config(fg="red", text="No account found!")

def view_transactions(username):
    try:
        with open(username, "r") as file:
            user_data = file.readlines()
            account_no = user_data[5].strip()
            balance = user_data[7].strip()  
        transactions = []  
        with open("TransactionLog.txt", "r") as file:
            for line in file:
                if line.startswith(username):
                    transactions.append(line.strip()) 
    except FileNotFoundError:
        messagebox.showerror("Error", "Transaction log file not found.")
        return

    # Create a new window for displaying transactions
    transactions_window = Toplevel(master)
    transactions_window.title('Transactions History')
    transactions_window.configure(bg='DeepSkyBlue4')

    # Display user's details and balance
    Label(transactions_window, text=f"Username: {username}", font=('Calibri', 12)).grid(row=0, columnspan=2, sticky=W, padx=10, pady=5)
    Label(transactions_window, text=f"Account Number: {account_no}", font=('Calibri', 12)).grid(row=1, columnspan=2, sticky=W, padx=10, pady=5)
    Label(transactions_window, text=f"Balance: R {balance}", font=('Calibri', 12, 'bold')).grid(row=2, columnspan=2, sticky=W, padx=10, pady=5)

    # Display transactions in a scrollable text widget
    scrollbar = Scrollbar(transactions_window)
    scrollbar.grid(row=3, column=1, sticky=NS)
    text = Text(transactions_window, wrap=WORD, yscrollcommand=scrollbar.set, font=('Calibri', 12))
    text.grid(row=3, column=0, sticky=NSEW, padx=10, pady=5)
    
    for transaction in transactions:
        text.insert(END, transaction + "\n")

    # Set scrollbar to scroll text widget
    scrollbar.config(command=text.yview)

    # Create a button to download transaction history
    Button(transactions_window, text="Download Transaction History", font=('Calibri', 12, 'bold'), command=lambda: download_transactions(username, transactions)).grid(row=4, columnspan=2, pady=10, sticky=W, padx=40)
    send_button = Button(transactions_window, text="Send to WhatsApp", command=lambda: send_to_whatsapp(username, transactions), font=('Calibri', 12, 'bold'))
    send_button.grid(row=4, columnspan=2, pady=10, sticky=E, padx= --40)
def download_transactions(username, transactions):
    download_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

    if download_location:
        with open(download_location, "w") as file:
            file.writelines(transactions)
        messagebox.showinfo("Success", "Transaction history downloaded successfully.")
   

def send_to_whatsapp(username, transactions):
    try:
        with open(username, "r") as file:
            user_data = file.readlines()
            cellphone = user_data[4].strip()

        if not transactions:
            messagebox.showinfo("Info", "No transactions to send.")
            return

        transaction_statement = "\n".join(transactions)
        pywhatkit.sendwhatmsg_instantly(f"+{cellphone}", transaction_statement)
        messagebox.showinfo("Success", "Transaction statement sent to your WhatsApp.")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        
def logout():
    master.destroy()  # Close the main window (master)
    
def pay_someone():
    pay_screen = Toplevel(master)
    pay_screen.title('Pay Someone')
    pay_screen.configure(bg='DeepSkyBlue4')

    Label(pay_screen, text="Recipient Name:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=W, padx=20, pady=10)
    recipient_name_entry = Entry(pay_screen, font=('Calibri', 14))
    recipient_name_entry.grid(row=0, column=1, padx=20, pady=10)

    Label(pay_screen, text="Recipient Account No:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=1, sticky=W, padx=20, pady=10)
    recipient_account_entry = Entry(pay_screen, font=('Calibri', 14))
    recipient_account_entry.grid(row=1, column=1, padx=20, pady=10)

    Label(pay_screen, text="Amount to Transfer (R):", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=2, sticky=W, padx=20, pady=10)
    transfer_amount_entry = Entry(pay_screen, font=('Calibri', 14))
    transfer_amount_entry.grid(row=2, column=1, padx=20, pady=10)

    def transfer_funds():
        recipient_name = recipient_name_entry.get()
        recipient_account = recipient_account_entry.get()
        transfer_amount = transfer_amount_entry.get()
        messagebox.showinfo("Success", "Transfer successful")

       
    Button(pay_screen, text="Transfer", command=transfer_funds, font=('Calibri', 14, 'bold'), fg='white', bg='RoyalBlue3').grid(row=3, columnspan=2, pady=20)



    
def transaction_screen():
    global temp_account_holder, temp_transaction, temp_transaction_amount, notif
  
    transaction_screen = Toplevel(master)
    transaction_screen.title('Transactions')
    transaction_screen.configure(bg='DeepSkyBlue4')

    # Labels
    Label(transaction_screen, text="Transaction Menu", font=('Calibri', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky=N, pady=10, padx=150)
    Label(transaction_screen, text="Please select an option:", font=('Calibri', 12)).grid(row=1, column=0, columnspan=2, sticky=N, pady=5, padx=150)

    # Buttons
    Button(transaction_screen, text="Personal Details", font=('Calibri', 12), width=30, command=personal_details).grid(row=2, column=0, padx=10, pady=5)
    Button(transaction_screen, text="Deposit", font=('Calibri', 12), width=30, command=deposit).grid(row=2, column=1, padx=10, pady=5)
    Button(transaction_screen, text="Withdraw", font=('Calibri', 12), width=30, command=withdraw).grid(row=3, column=0, padx=10, pady=5)
    Button(transaction_screen, text="Pay Someone", font=('Calibri', 12), width=30, command=pay_someone).grid(row=3, column=1, padx=10, pady=5)
    Button(transaction_screen, text="View Transactions", font=('Calibri', 12), width=30, command=lambda: view_transactions(login_name)).grid(row=4, column=0, padx=10, pady=5)
    Button(transaction_screen, text="Logout", font=('Calibri', 12, 'bold'), width=30, command=logout).grid(row=4, column=1, padx=10, pady=5)


def personal_details():
    # Vars
    file = open(login_name, 'r')
    user_details = file.readlines()
    file.close()
    details_name = user_details[0].strip()
    details_age = user_details[2].strip()
    details_gender = user_details[3].strip()
    account_no = user_details[5].strip()
    image_path = user_details[6].strip()
    details_balance = user_details[7].strip()
    
   
    personal_details_screen = Toplevel(master)
    personal_details_screen.title('Personal Details')
    personal_details_screen.configure(bg='DeepSkyBlue4')

    
    Label(personal_details_screen, text="Personal Details", font=('Calibri', 16, 'bold'), bg='DeepSkyBlue4', fg='white').grid(row=0, columnspan=2, pady=10)
    if os.path.exists(image_path):
        user_image = Image.open(image_path)
        user_image = user_image.resize((150, 150))
        user_image = ImageTk.PhotoImage(user_image)
        Label(personal_details_screen, image=user_image, bg='DeepSkyBlue4').grid(row=1, columnspan=2, pady=10)
       
        personal_details_screen.image = user_image

    Label(personal_details_screen, text="Name:", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=2, column=0, sticky=W, padx=20, pady=5)
    Label(personal_details_screen, text=details_name, font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=2, column=1, sticky=W, padx=20, pady=5)

    Label(personal_details_screen, text="Account No:", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=3, column=0, sticky=W, padx=20, pady=5)
    Label(personal_details_screen, text=account_no, font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=3, column=1, sticky=W, padx=20, pady=5)

    Label(personal_details_screen, text="Age:", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=4, column=0, sticky=W, padx=20, pady=5)
    Label(personal_details_screen, text=details_age, font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=4, column=1, sticky=W, padx=20, pady=5)

    Label(personal_details_screen, text="Gender:", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=5, column=0, sticky=W, padx=20, pady=5)
    Label(personal_details_screen, text=details_gender, font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=5, column=1, sticky=W, padx=20, pady=5)

    Label(personal_details_screen, text=f"Balance: R {details_balance}", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=6, columnspan=2, sticky=W, padx=20, pady=5)


def deposit():
   
    file = open(login_name, 'r')
    user_data = file.readlines()
    cellphone = user_data[4]
    balance = float(user_data[7].strip())  
    file.close()
    
  
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
        
       
        file = open(login_name, 'r+')
        user_data = file.readlines()
        balance = float(user_data[7]) 
        new_balance = balance + deposit_amount
        
        
        user_data[7] = str(new_balance) + '\n'
        file.seek(0)
        file.writelines(user_data)
        file.close()
        
        # Log deposit transaction
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"{login_name}: Deposit: {deposit_amount}\n")
        
        deposit_notif.config(fg="green", text=f"Deposit successful. New Balance: R{new_balance}")
        current_balance_label.config(text=f"R{new_balance}")
        send_sms_notification(cellphone, f"R {deposit_amount} deposited successfully into your account. New balance is R {balance}.")
       

    deposit_screen = Toplevel(master)
    deposit_screen.title("Deposit")
    deposit_screen.configure(bg='DeepSkyBlue4')
    
    # Labels and Entry
    Label(deposit_screen, text="Current Balance:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, column=0, padx=10, pady=10, sticky=W)
    current_balance_label = Label(deposit_screen, text=f"R{balance}", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
    current_balance_label.grid(row=0, column=1, padx=10, pady=10, sticky=E)
    
    Label(deposit_screen, text="How much would you like to deposit:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=1, column=0, padx=10, pady=10, sticky=W)
    deposit_entry = Entry(deposit_screen, font=('Calibri', 14))
    deposit_entry.grid(row=1, column=1, padx=10, pady=10, sticky=E)
    
    # Button and Notification Label
    Button(deposit_screen, text="Deposit", font=('Calibri', 14, 'bold'), fg='white', bg='RoyalBlue3', command=finish_deposit).grid(row=2, column=0, columnspan=2, padx=10, pady=20)
    deposit_notif = Label(deposit_screen, font=('Calibri', 12), bg='DeepSkyBlue4')
    deposit_notif.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def withdraw():
    file = open(login_name, 'r')
    user_data = file.readlines()
    cellphone = user_data[4]
    balance = float(user_data[7].strip()) 
    file.close()
    
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
        
        
        file = open(login_name, 'r+')
        user_data = file.readlines()
        balance = float(user_data[7]) 
        
        if withdrawal_amount > balance:
            withdrawal_notif.config(fg="red", text="Insufficient funds.")
            file.close()
            return
        
        new_balance = balance - withdrawal_amount
        
       
        user_data[7] = str(new_balance) + '\n'
        file.seek(0)
        file.writelines(user_data)
        file.close()
        
       
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(f"{login_name}: Withdrawal: {withdrawal_amount}\n")
        
        withdrawal_notif.config(fg="green", text=f"Withdrawal successful. New Balance: R{new_balance}")
        current_balance_label.config(text=f"R{new_balance}")
        send_sms_notification(cellphone, f"R {withdrawal_amount} withdrawn successfully from your account. New balance is R {new_balance}.")
        
    withdrawal_screen = Toplevel(master)
    withdrawal_screen.title("Withdrawal")
    withdrawal_screen.configure(bg='DeepSkyBlue4') 
    
    Label(withdrawal_screen, text="Current Balance:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, column=0, padx=10, pady=10, sticky=W)
    current_balance_label = Label(withdrawal_screen, text=f"R{balance}", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
    current_balance_label.grid(row=0, column=1, padx=10, pady=10, sticky=E)
    
    Label(withdrawal_screen, text="How much would you like to withdraw:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=1, column=0, padx=10, pady=10, sticky=W)
    withdrawal_entry = Entry(withdrawal_screen, font=('Calibri', 14))
    withdrawal_entry.grid(row=1, column=1, padx=10, pady=10, sticky=E)
    
    # Button and Notification Label
    Button(withdrawal_screen, text="Withdraw", font=('Calibri', 14, 'bold'), fg='white', bg='RoyalBlue3', command=finish_withdrawal).grid(row=2, column=0, columnspan=2, padx=10, pady=20)
    withdrawal_notif = Label(withdrawal_screen, font=('Calibri', 12), bg='DeepSkyBlue4')
    withdrawal_notif.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


def login_screen():
    global login_screen
    login_screen = Toplevel(master)
    login_screen.title('Login')
    login_screen.configure(bg='DeepSkyBlue4')

    # Labels
    Label(login_screen, text="Login", font=('Calibri', 16, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10, padx=20)
    Label(login_screen, text="Username", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4').grid(row=1, sticky=W, pady=5, padx=20)
    Label(login_screen, text="Password", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4').grid(row=2, sticky=W, pady=5, padx=20)

    # Entries
    global temp_login_name
    temp_login_name = StringVar()
    Entry(login_screen, textvariable=temp_login_name, font=('Calibri', 14)).grid(row=1, column=1, padx=20, pady=5)
    global temp_login_password
    temp_login_password = StringVar()
    password_entry = Entry(login_screen, textvariable=temp_login_password, show="*", font=('Calibri', 14))
    password_entry.grid(row=2, column=1, padx=20, pady=5)

    # Show password checkbox
    show_password_var = BooleanVar()
    show_password_checkbox = Checkbutton(login_screen, text="Show Password", variable=show_password_var, command=lambda: toggle_password_visibility(password_entry, show_password_var), font=('Calibri', 12), fg='white', bg='DeepSkyBlue4')
    show_password_checkbox.grid(row=3, columnspan=2, pady=5)

    # Buttons
    Button(login_screen, text="Login", command=login_session, font=('Calibri', 12, 'bold'), width=15, fg='white', bg='RoyalBlue3').grid(row=4, columnspan=2, sticky=N, pady=10)

def toggle_password_visibility(password_entry, show_password_var):
    show_password = show_password_var.get()
    password_entry.config(show="" if show_password else "*")

# Image import
img = Image.open('secure.png')
img = img.resize((150, 150))
img = ImageTk.PhotoImage(img)

# Labels
Label(master, text="Transact Bank", font=('Calibri', 22, 'bold'), fg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10)
Label(master, text="Bank Better with Transact Bank! \n The most secure bank in the southern hemisphere!", font=('Calibri', 15)).grid(row=1, sticky=N, padx=15)
Label(master, image=img).grid(row=2, sticky=N, pady=15)

# Buttons
Button(master, text="Register", font=('Calibri', 12, 'bold'), width=20, command=register, fg='white', bg='RoyalBlue3').grid(row=3, sticky=N, pady=5)
Button(master, text="Login", font=('Calibri', 12, 'bold'), width=20, command=login_screen, fg='white', bg='RoyalBlue3').grid(row=4, sticky=N, pady=10)

# Footer
footer_text = "Contact the Transact Bank Tech Team for any issues relating to the app on 0861 084 567."
Label(master, text=footer_text, font=('Calibri', 12, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=10, sticky=S, pady=20, columnspan=2)

master.mainloop()


