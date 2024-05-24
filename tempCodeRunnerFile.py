def login_session():
    global login_name, login_notif
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    # Ensure login_notif is defined at the correct place
    login_notif = Label(login_screen, font=('Calibri', 12), bg='DeepSkyBlue4') # Define the login_notif variable
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
                Label(account_dashboard, text="Account Dashboard", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10, padx=150) 
                Label(account_dashboard, text="Welcome " + name + "\n\nWould you like to make a transaction?", font=('Calibri', 12)).grid(row=2, sticky=N, pady=5, padx=150)
                # Display user image
                user_image_path = file_data[6]  # Image path is stored in the 7th line
                if os.path.exists(user_image_path):
                    user_image = Image.open(user_image_path)
                    user_image = user_image.resize((150, 150))
                    user_image = ImageTk.PhotoImage(user_image)
                    Label(account_dashboard, image=user_image, bg='DeepSkyBlue4').grid(row=1, sticky=N, pady=5)
                    # Keep a reference to the image object to prevent garbage collection
                    account_dashboard.image = user_image
                # Buttons
                Button(account_dashboard, text="Yes", width=20, command=transaction_screen, font=('Calibri', 12)).grid(row=3, sticky=N, pady=5)
                Button(account_dashboard, text="No", width=20, command=account_dashboard.destroy, font=('Calibri', 12)).grid(row=4, sticky=N, pady=5)
                send_sms_notification(cellphone, f"Login successful for {name}.")
                return
            else:
                login_notif.config(fg="red", text="Password incorrect!")
                return
    login_notif.config(fg="red", text="No account found!")