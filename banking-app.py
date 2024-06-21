import os
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import random
import string
import requests

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

class BankingApp:
    def __init__(self, master):
        self.master = master
        self.master.title('Banking App')
        self.master.configure(bg='DeepSkyBlue4')

        self.frames = {}

        for F in (StartPage, RegisterPage, LoginPage, DashboardPage, TransactionPage):
            page_name = F.__name__
            frame = F(parent=self.master, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def login(self, username, password):
        all_accounts = os.listdir()
        for name in all_accounts:
            if name == username:
                file = open(name, "r")
                file_data = file.read().split('\n')
                file.close()
                if file_data[1] == password:
                    self.current_user = name
                    self.user_data = file_data
                    self.show_frame("DashboardPage")
                    return True
                else:
                    return False
        return False

    def register(self, name, age, gender, cellphone, image):
        if os.path.exists(name):
            return False, "Account already exists"
        if not age.isdigit() or int(age) < 16:
            return False, "Minimum age is 16 years"
        if not self.validate_cellphone(cellphone):
            return False, "Invalid cellphone number"
        
        account_number = generate_account_number()
        password = generate_password()

        with open(name, "w") as new_file:
            new_file.write(f"{name}\n{password}\n{age}\n{gender}\n{cellphone}\n{account_number}\n{image}\n0")

        self.current_user = name
        self.user_data = [name, password, age, gender, cellphone, account_number, image, "0"]
        self.show_frame("DashboardPage")
        return True, f"Account created successfully!\nAccount Number: {account_number}\nPassword: {password}"

    def validate_cellphone(self, cellphone):
        if len(cellphone) != 10 or not cellphone.startswith('0') or not cellphone.isdigit():
            return False
        return True

    def update_balance(self, username, new_balance):
        with open(username, 'r+') as file:
            user_data = file.readlines()
            user_data[7] = str(new_balance) + '\n'
            file.seek(0)
            file.writelines(user_data)

    def record_transaction(self, transaction_details):
        with open("TransactionLog.txt", "a") as log_file:
            log_file.write(transaction_details + "\n")

    def get_balance(self, username):
        with open(username, 'r') as file:
            return float(file.readlines()[7].strip())

class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='DeepSkyBlue4')
        self.controller = controller

        Label(self, text="Transact Bank", font=('Calibri', 22, 'bold'), fg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10)
        Label(self, text="Bank Better with Transact Bank!\nThe most secure bank in the southern hemisphere!", font=('Calibri', 15)).grid(row=1, sticky=N, padx=15)

        self.img = Image.open('secure.png')
        self.img = self.img.resize((150, 150))
        self.img = ImageTk.PhotoImage(self.img)
        Label(self, image=self.img).grid(row=2, sticky=N, pady=15)

        Button(self, text="Register", font=('Calibri', 12, 'bold'), width=20, command=lambda: controller.show_frame("RegisterPage"), fg='white', bg='RoyalBlue3').grid(row=3, sticky=N, pady=5)
        Button(self, text="Login", font=('Calibri', 12, 'bold'), width=20, command=lambda: controller.show_frame("LoginPage"), fg='white', bg='RoyalBlue3').grid(row=4, sticky=N, pady=10)

class RegisterPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='DeepSkyBlue4')
        self.controller = controller

        Label(self, text="Register", font=('Calibri', 22, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10, padx=20)
        self.notif = Label(self, font=('Calibri', 12), fg='red', bg='DeepSkyBlue4')
        self.notif.grid(row=7, columnspan=2, sticky=N, pady=10)

        self.temp_name = StringVar()
        self.temp_age = StringVar()
        self.temp_gender = StringVar()
        self.temp_cellphone = StringVar()

        Label(self, text="Name", font=('Calibri', 12), fg='white', bg='DeepSkyBlue4').grid(row=1, sticky=W, pady=2, padx=20)
        Entry(self, textvariable=self.temp_name).grid(row=1, column=1, padx=30)

        Label(self, text="Age", font=('Calibri', 12), fg='white', bg='DeepSkyBlue4').grid(row=2, sticky=W, pady=2, padx=20)
        Entry(self, textvariable=self.temp_age).grid(row=2, column=1, padx=30)

        Label(self, text="Gender", font=('Calibri', 12), fg='white', bg='DeepSkyBlue4').grid(row=3, sticky=W, pady=2, padx=20)
        gender_options = ["Male", "Female", "Other"]
        gender_combobox = Combobox(self, textvariable=self.temp_gender, values=gender_options, state="readonly")
        gender_combobox.grid(row=3, column=1, padx=30)
        gender_combobox.set("Select")

        Label(self, text="Cellphone", font=('Calibri', 12), fg='white', bg='DeepSkyBlue4').grid(row=4, sticky=W, pady=2, padx=20)
        Entry(self, textvariable=self.temp_cellphone).grid(row=4, column=1, padx=30)

        self.image_entry = Entry(self)
        self.image_entry.grid(row=5, column=0, padx=30, pady=5)
        upload_button = Button(self, text="Upload Image", command=self.upload_image, font=('Calibri', 10), fg='white', bg='RoyalBlue3')
        upload_button.grid(row=5, column=1, padx=30, pady=5)

        Button(self, text="Register", command=self.finish_reg, font=('Calibri', 12, 'bold'), width=15, fg='white', bg='RoyalBlue3').grid(row=6, columnspan=2, sticky=N, pady=10)

    def upload_image(self):
        image_path = filedialog.askopenfilename()
        self.image_entry.delete(0, END)
        self.image_entry.insert(0, image_path)

    def finish_reg(self):
        name = self.temp_name.get()
        age = self.temp_age.get()
        gender = self.temp_gender.get()
        cellphone = self.temp_cellphone.get()
        image = self.image_entry.get()

        success, message = self.controller.register(name, age, gender, cellphone, image)
        if success:
            self.notif.config(fg="green", text=message)
        else:
            self.notif.config(fg="red", text=message)

class LoginPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='DeepSkyBlue4')
        self.controller = controller

        Label(self, text="Login", font=('Calibri', 22, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10, padx=20)
        self.login_notif = Label(self, font=('Calibri', 12), fg='red', bg='DeepSkyBlue4')
        self.login_notif.grid(row=5, columnspan=2, sticky=N, pady=10)

        self.temp_login_name = StringVar()
        self.temp_login_password = StringVar()

        Label(self, text="Username", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4').grid(row=1, sticky=W, pady=5, padx=20)
        Entry(self, textvariable=self.temp_login_name, font=('Calibri', 14)).grid(row=1, column=1, padx=20, pady=5)

        Label(self, text="Password", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4').grid(row=2, sticky=W, pady=5, padx=20)
        password_entry = Entry(self, textvariable=self.temp_login_password, show="*", font=('Calibri', 14))
        password_entry.grid(row=2, column=1, padx=20, pady=5)

        show_password_var = BooleanVar()
        show_password_checkbox = Checkbutton(self, text="Show Password", variable=show_password_var, command=lambda: self.toggle_password_visibility(password_entry, show_password_var), font=('Calibri', 12), fg='white', bg='DeepSkyBlue4')
        show_password_checkbox.grid(row=3, columnspan=2, pady=5)

        Button(self, text="Login", command=self.login, font=('Calibri', 12, 'bold'), width=15, fg='white', bg='RoyalBlue3').grid(row=4, columnspan=2, sticky=N, pady=10)

    def toggle_password_visibility(self, password_entry, show_password_var):
        show_password = show_password_var.get()
        password_entry.config(show="" if show_password else "*")

    def login(self):
        username = self.temp_login_name.get()
        password = self.temp_login_password.get()
        success = self.controller.login(username, password)
        if success:
            self.login_notif.config(fg="green", text="Login successful!")
        else:
            self.login_notif.config(fg="red", text="Invalid credentials")

class DashboardPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='DeepSkyBlue4')
        self.controller = controller

        self.notif = Label(self, font=('Calibri', 12), fg='red', bg='DeepSkyBlue4')
        self.notif.grid(row=7, columnspan=2, sticky=N, pady=10)

        Label(self, text="Account Dashboard", font=('Calibri', 22, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, sticky=N, pady=10, padx=20)
        self.welcome_msg = Label(self, text="Welcome!", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
        self.welcome_msg.grid(row=1, sticky=N, pady=5, padx=20)

        self.balance_msg = Label(self, text="Your Balance: R0", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
        self.balance_msg.grid(row=2, sticky=N, pady=5, padx=20)

        Button(self, text="Personal Details", font=('Calibri', 12), width=30, command=self.view_personal_details).grid(row=3, padx=10, pady=5)
        Button(self, text="Deposit", font=('Calibri', 12), width=30, command=self.deposit).grid(row=4, padx=10, pady=5)
        Button(self, text="Withdraw", font=('Calibri', 12), width=30, command=self.withdraw).grid(row=5, padx=10, pady=5)
        Button(self, text="Pay Someone", font=('Calibri', 12), width=30, command=self.pay_someone).grid(row=6, padx=10, pady=5)
        Button(self, text="View Transactions", font=('Calibri', 12), width=30, command=self.view_transactions).grid(row=7, padx=10, pady=5)
        Button(self, text="Logout", font=('Calibri', 12, 'bold'), width=30, command=self.logout).grid(row=8, padx=10, pady=5)

    def update_dashboard(self):
        user_details = self.controller.user_data
        self.welcome_msg.config(text=f"Welcome, {user_details[0]}")
        balance = self.controller.get_balance(user_details[0])
        self.balance_msg.config(text=f"Your Balance: R{balance}")

    def view_personal_details(self):
        user_details = self.controller.user_data
        details_screen = Toplevel(self.controller.master)
        details_screen.title('Personal Details')
        details_screen.configure(bg='DeepSkyBlue4')

        Label(details_screen, text="Personal Details", font=('Calibri', 16, 'bold'), bg='DeepSkyBlue4', fg='white').grid(row=0, columnspan=2, pady=10)
        if os.path.exists(user_details[6]):
            user_image = Image.open(user_details[6])
            user_image = user_image.resize((150, 150))
            user_image = ImageTk.PhotoImage(user_image)
            Label(details_screen, image=user_image, bg='DeepSkyBlue4').grid(row=1, columnspan=2, pady=10)
            details_screen.image = user_image

        details = [("Name", user_details[0]), ("Account No", user_details[5]), ("Age", user_details[2]), ("Gender", user_details[3]), ("Balance", f"R{user_details[7].strip()}")]
        for i, (label, value) in enumerate(details, start=2):
            Label(details_screen, text=f"{label}:", font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=i, column=0, sticky=W, padx=20, pady=5)
            Label(details_screen, text=value, font=('Calibri', 14), bg='DeepSkyBlue4', fg='white').grid(row=i, column=1, sticky=W, padx=20, pady=5)

    def deposit(self):
        deposit_screen = Toplevel(self.controller.master)
        deposit_screen.title("Deposit")
        deposit_screen.configure(bg='DeepSkyBlue4')

        current_balance = self.controller.get_balance(self.controller.current_user)
        Label(deposit_screen, text="Current Balance:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, column=0, padx=10, pady=10, sticky=W)
        current_balance_label = Label(deposit_screen, text=f"R{current_balance}", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
        current_balance_label.grid(row=0, column=1, padx=10, pady=10, sticky=E)

        Label(deposit_screen, text="How much would you like to deposit:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=1, column=0, padx=10, pady=10, sticky=W)
        deposit_entry = Entry(deposit_screen, font=('Calibri', 14))
        deposit_entry.grid(row=1, column=1, padx=10, pady=10, sticky=E)

        def finish_deposit():
            deposit_amount = deposit_entry.get()
            if not deposit_amount:
                self.notif.config(fg="red", text="Please enter an amount.")
                return
            try:
                deposit_amount = float(deposit_amount)
                if deposit_amount <= 0:
                    self.notif.config(fg="red", text="Invalid amount. Please enter a positive amount.")
                    return
            except ValueError:
                self.notif.config(fg="red", text="Invalid input. Please enter a valid amount.")
                return

            new_balance = current_balance + deposit_amount
            self.controller.update_balance(self.controller.current_user, new_balance)
            self.controller.record_transaction(f"{self.controller.current_user}: Deposit: {deposit_amount}")
            self.notif.config(fg="white", text=f"Deposit successful. New Balance: R{new_balance}")
            current_balance_label.config(text=f"R{new_balance}")
            self.update_dashboard()

        Button(deposit_screen, text="Deposit", font=('Calibri', 14, 'bold'), fg='white', bg='RoyalBlue3', command=finish_deposit).grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def withdraw(self):
        withdraw_screen = Toplevel(self.controller.master)
        withdraw_screen.title("Withdrawal")
        withdraw_screen.configure(bg='DeepSkyBlue4')

        current_balance = self.controller.get_balance(self.controller.current_user)
        Label(withdraw_screen, text="Current Balance:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=0, column=0, padx=10, pady=10, sticky=W)
        current_balance_label = Label(withdraw_screen, text=f"R{current_balance}", font=('Calibri', 14), fg='white', bg='DeepSkyBlue4')
        current_balance_label.grid(row=0, column=1, padx=10, pady=10, sticky=E)

        Label(withdraw_screen, text="How much would you like to withdraw:", font=('Calibri', 14, 'bold'), fg='white', bg='DeepSkyBlue4').grid(row=1, column=0, padx=10, pady=10, sticky=W)
        withdraw_entry = Entry(withdraw_screen, font=('Calibri', 14))
        withdraw_entry.grid(row=1, column=1, padx=10, pady=10, sticky=E)

        def finish_withdrawal():
            withdrawal_amount = withdraw_entry.get()
            if not withdrawal_amount:
                self.notif.config(fg="red", text="Please enter an amount.")
                return
            try:
                withdrawal_amount = float(withdrawal_amount)
                if withdrawal_amount <= 0:
                    self.notif.config(fg="red", text="Invalid amount. Please enter a positive amount.")
                    return
            except ValueError:
                self.notif.config(fg="red", text="Invalid input. Please enter a valid amount.")
                return

            if withdrawal_amount > current_balance:
                self.notif.config(fg="red", text="Insufficient funds.")
                return

            new_balance = current_balance - withdrawal_amount
            self.controller.update_balance(self.controller.current_user, new_balance)
            self.controller.record_transaction(f"{self.controller.current_user}: Withdrawal: {withdrawal_amount}")
            self.notif.config(fg="white", text=f"Withdrawal successful. New Balance: R{new_balance}")
            current_balance_label.config(text=f"R{new_balance}")
            self.update_dashboard()

        Button(withdraw_screen, text="Withdraw", font=('Calibri', 14, 'bold'), fg='white', bg='RoyalBlue3', command=finish_withdrawal).grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    def pay_someone(self):
        pay_screen = Toplevel(self.controller.master)
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

        def validate_and_transfer():
            recipient_name = recipient_name_entry.get()
            recipient_account = recipient_account_entry.get()
            transfer_amount = transfer_amount_entry.get()

            if not recipient_name:
                messagebox.showerror("Input Error", "Please enter the recipient's name.")
                return
            if not recipient_account:
                messagebox.showerror("Input Error", "Please enter the recipient's account number.")
                return
            if not transfer_amount:
                messagebox.showerror("Input Error", "Please enter the amount to transfer.")
                return

            try:
                transfer_amount = float(transfer_amount)
                if transfer_amount <= 0:
                    messagebox.showerror("Input Error", "Invalid amount. Please enter a positive amount.")
                    return
            except ValueError:
                messagebox.showerror("Input Error", "Invalid input. Please enter a valid amount.")
                return

            current_balance = self.controller.get_balance(self.controller.current_user)
            if transfer_amount > current_balance:
                messagebox.showerror("Error", "Insufficient funds.")
                return

            # Deduct from sender
            new_sender_balance = current_balance - transfer_amount
            self.controller.update_balance(self.controller.current_user, new_sender_balance)
            self.controller.record_transaction(f"{self.controller.current_user}: Transfer to {recipient_name} ({recipient_account}): {transfer_amount}")

            # Add to recipient
            if not os.path.exists(recipient_name):
                messagebox.showerror("Error", "Recipient account not found.")
                return

            recipient_balance = self.controller.get_balance(recipient_name)
            new_recipient_balance = recipient_balance + transfer_amount
            self.controller.update_balance(recipient_name, new_recipient_balance)
            self.controller.record_transaction(f"{recipient_name}: Received from {self.controller.current_user}: {transfer_amount}")

            self.notif.config(fg="white", text=f"Transfer successful. New Balance: R{new_sender_balance}")
            self.update_dashboard()
            messagebox.showinfo("Success", "Transfer successful")

        Button(pay_screen, text="Transfer", command=validate_and_transfer, font=('Calibri', 12, 'bold'), fg='white', bg='RoyalBlue3').grid(row=3, columnspan=2, pady=20)

    def view_transactions(self):
        try:
            transactions = []
            with open("TransactionLog.txt", "r") as file:
                for line in file:
                    if line.startswith(self.controller.current_user):
                        transactions.append(line.strip())

            transactions_window = Toplevel(self.controller.master)
            transactions_window.title('Transactions History')
            transactions_window.configure(bg='DeepSkyBlue4')

            user_details = self.controller.user_data
            balance = self.controller.get_balance(self.controller.current_user)

            Label(transactions_window, text=f"Username: {user_details[0]}", font=('Calibri', 12)).grid(row=0, columnspan=2, sticky=W, padx=10, pady=5)
            Label(transactions_window, text=f"Account Number: {user_details[5]}", font=('Calibri', 12)).grid(row=1, columnspan=2, sticky=W, padx=10, pady=5)
            Label(transactions_window, text=f"Balance: R {balance}", font=('Calibri', 12, 'bold')).grid(row=2, columnspan=2, sticky=W, padx=10, pady=5)

            scrollbar = Scrollbar(transactions_window)
            scrollbar.grid(row=3, column=1, sticky=NS)
            text = Text(transactions_window, wrap=WORD, yscrollcommand=scrollbar.set, font=('Calibri', 12))
            text.grid(row=3, column=0, sticky=NSEW, padx=10, pady=5)
            for transaction in transactions:
                text.insert(END, transaction + "\n")

            scrollbar.config(command=text.yview)

            Button(transactions_window, text="Download Transaction History", font=('Calibri', 12, 'bold'), command=lambda: self.download_transactions(transactions)).grid(row=4, columnspan=2, pady=10, sticky=W, padx=40)

        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.")
            return

    def download_transactions(self, transactions):
        download_location = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if download_location:
            with open(download_location, "w") as file:
                file.writelines("\n".join(transactions))
            messagebox.showinfo("Success", "Transaction history downloaded successfully.")

    def logout(self):
        self.controller.show_frame("StartPage")

class TransactionPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='DeepSkyBlue4')
        self.controller = controller

if __name__ == "__main__":
    root = Tk()
    root.geometry("600x400")
    app = BankingApp(master=root)
    root.mainloop()