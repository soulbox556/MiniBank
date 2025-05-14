# ----------------------------------------------------------------------
#  v1 Ertan: first code
# v1.1 Ertan: with some specifications
# v.1.2 Ertan: hide passwords
# v.1.3 Ertan: authomatic acount number example
# v.1.4 Ertan: Eshte finalizuar fajli dhe tani do te punohet permes github : EI MA
#
# v.1.5 Majlini ka punuar 05/04/2025
#   1. Me mujt me kriju account
#   2. ⁠printat ne console dalin me ngjyra
#   3. ⁠edhe userat ruhen ne nje file
#
# v.1.6 Majlind: Fix read and write users to file and fix login loop
# v.1.7 Majlind:
#   1. Fix create user with empty username and password
#   2. Make possible to return back on menu by entering
# v1.8 EI+MA (with logging)
#  1.8.1 included via a logs.json file all acctivities The logging function log_activity is used throughout the application to record key actions
# -----------------------------------------------------------------------------------
import hashlib
import json
import os
import pwinput
from datetime import datetime
import AppPrints as pr


def log_activity(action, username=None, details=None):
    log_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'logs.json')
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "username": username or "SYSTEM",
        "action": action,
        "details": details or ""
    }
    try:
        if os.path.exists(log_file_path):
            with open(log_file_path, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
    except (FileNotFoundError, json.JSONDecodeError):
        logs = []

    logs.append(log_entry)
    with open(log_file_path, 'w') as f:
        json.dump(logs, f, indent=4)


class BankAccount:
    def __init__(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance
        self.transaction_counter = 10000

    def deposit(self, amount):
        self.balance += amount
        log_activity("Deposit", self.account_name,
                     f"Account: {self.account_number}, Amount: {amount}")
        pr.success(
            f"Deposited €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.balance:
            pr.error("Insufficient funds.")
        elif amount > 500:
            pr.error("Max withdrawal amount is 500€.")
        else:
            self.balance -= amount
            log_activity("Withdraw", self.account_name,
                         f"Account: {self.account_number}, Amount: {amount}")
            pr.success(
                f"Withdrew €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def check_balance(self):
        pr.success(f"Current balance is €{self.balance:.2f}.")

    def transfer(self, amount, recipient_account, sender_username, bank_system):
        if amount > self.balance:
            pr.error("Insufficient funds.")
        elif amount > 1000:
            pr.error("Max transfer amount is 1000€.")
        else:
            self.balance -= amount
            recipient_account.balance += amount
            log_activity("Transfer", self.account_name,
                         f"From: {self.account_number}, To: {recipient_account.account_number}, Amount: {amount}")
            pr.success(
                f"Transferred €{amount:.2f} to account {recipient_account.account_number}. New balance is €{self.balance:.2f}.")
            # Save transfer to JSON
            transfer_data = {
                "from": self.account_number,
                "to": recipient_account.account_number,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
            bank_system.users[sender_username]["transfers"].append(transfer_data)
            bank_system.save_users_to_file()

    def pay_bill(self, company, amount, bank_system, username):
        allowed_companies = {
            "EC": "The Bright Light Electric Company (EC)",
            "CQ": "Credit Card Company Q (CQ)",
            "FI": "Fast Internet, Inc. (FI)"
        }

        if company not in allowed_companies:
            pr.error("Company not recognized. Must be EC, CQ, or FI.")
            return False

        if amount > 2000:
            pr.error("Cannot pay more than €2000 in a single session.")
            return False

        if self.balance - amount < 0:
            pr.error("Insufficient funds to pay the bill.")
            return False

        self.balance -= amount
        timestamp = datetime.now().isoformat()

        # Save to logs.json
        log_activity("Bill Payment", username,
                     f"Paid {amount:.2f} to {allowed_companies[company]} from account {self.account_number}")

        # Save in users.json
        if "bills" not in bank_system.users[username]:
            bank_system.users[username]["bills"] = []
        bank_system.users[username]["bills"].append({
            "from": self.account_number,
            "company": allowed_companies[company],
            "amount": amount,
            "timestamp": timestamp
        })

        bank_system.save_users_to_file()

        pr.success(
            f"Successfully paid €{amount:.2f} to {allowed_companies[company]}. New balance: €{self.balance:.2f}")
        return True



class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.users = self.load_users_from_file()
        self.user_accounts = {}
        self.account_counter = 10000

    def get_users_file_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')

    def load_users_from_file(self):
        try:
            with open(self.get_users_file_path(), 'r') as file:
                users_data = json.load(file)
                return users_data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_users_to_file(self):
        with open(self.get_users_file_path(), 'w') as file:
            json.dump(self.users, file, indent=4)

    def _generate_account_number(self, account_name, initial_balance):
        cc = "05"
        name_part = account_name.upper().replace(" ", "_")[:20].ljust(20, "_")
        acc_num = f"{self.account_counter:05d}"
        self.account_counter += 1
        amount = f"{int(initial_balance * 100):08d}"
        mm = f"{datetime.now().month:02d}"
        return f"{cc}_{name_part}_{acc_num}_{amount}_{mm}"

    def create_account(self, username, account_name, initial_balance=0, save=True):
        if username not in self.users:
            pr.warning("User not found.")
            return
        
        # Check if the user already has an account with the same name
        for acc_num in self.get_user_accounts(username):
            acc = self.accounts.get(acc_num)
            if acc and acc.account_name.lower() == account_name.lower():
                pr.error("You already have an account with this name.")
                return

        account_number = self._generate_account_number(
            account_name, initial_balance)
        new_account = BankAccount(
            account_number, account_name, initial_balance)
        self.accounts[account_number] = new_account
        self._add_user_account(username, account_number)
        # Save account info to users.json
        account_data = {
            "account_number": account_number,
            "account_name": account_name,
            "balance": initial_balance
        }
        self.users[username]["accounts"].append(account_data)
        if save:
            self.save_users_to_file()

        log_activity("Account created", username,
                     f"Account Number: {account_number}, Initial Balance: {initial_balance}")
        pr.success(
            f"Account created successfully!\nYour new account number: {account_number}")

    def _add_user_account(self, username, account_number):
        if username not in self.user_accounts:
            self.user_accounts[username] = []
        self.user_accounts[username].append(account_number)

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def get_user_accounts(self, username):
        return self.user_accounts.get(username, [])

    def list_user_accounts(self, username):
        if username not in self.user_accounts:
            pr.warning("No accounts found.")
            return
        for acc_num in self.user_accounts[username]:
            account = self.accounts[acc_num]
            pr.success(
                f"Account {acc_num}: {account.account_name} - €{account.balance:.2f}")

    def create_user(self, username, password, save):
        if not username or not password:
            pr.error("Username and password cannot be empty.")
            return
        if username in self.users:
            pr.error("Username already exists.")
            return
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = {
            "password": hashed_pw,
            "accounts": [],
            "transfers": []
        }
        if save:
            self.save_users_to_file()
        log_activity("User registered", username)
        pr.success(f"User {username} created.")

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save_users_to_file()

    def authenticate_user(self, username, password):
        if username in self.users:
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            return self.users[username]["password"] == hashed_pw
        return False


def validate_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                pr.error("Amount must be positive.")
                continue
            return value
        except ValueError:
            pr.error("Invalid input. Please enter a number.")


def display_home_page():
    pr.header("\n--- Welcome to Mini Bank ---")
    pr.header("\n--- This was created for base for Master AAB Project ---")
    pr.header("\n--- students for this project are: \nStudent: Fatmir Hasani - Frontend / Product Analyst\nStudent: Lendrit Berisha - Frontend / Product Analyst\nStudent: Majlind Avdylaj - Lead Programmer / Test\nStudent: Ertan Iliyaz - Backend programmer / Documentation\nMentor: Prof. Ass. Dr. Ramadan Dervishi (Product Owner)\n---")
    pr.menu("1. Login")
    pr.menu("2. Register")
    pr.menu("3. Exit")

    while True:
        choice = input("Choose option (1-3): ")

        if choice == "1":
            return "login"
        elif choice == "2":
            return "register"
        elif choice == "3":
            pr.warning("Exiting application.")
            log_activity("Application exit")
            return "exit"
        pr.error("Invalid choice.")


def login_page(bank):
    pr.header("\n--- Login ---")
    pr.menu("Enter 0 to go back.")
    username = input("Username: ").strip()
    if username == "0":
        return None

    password = pwinput.pwinput("Password: ").strip()
    if password == "0":
        return None

    if bank.authenticate_user(username, password):
        pr.success(f"Welcome {username}!")
        log_activity("User login", username)
        # Load accounts from JSON
        user_data = bank.users[username]
        for acc in user_data.get("accounts", []):
            account_number = acc["account_number"]
            account_name = acc["account_name"]
            balance = acc["balance"]

            # Create BankAccount object and store in bank.accounts
            account = BankAccount(account_number, account_name, balance)
            bank.accounts[account_number] = account

            # Also track account numbers for this user
            bank._add_user_account(username, account_number)
        return username
    pr.error("Invalid credentials.")
    return None


def register_page(bank):
    pr.header("\n--- Register ---")
    pr.menu("Enter 0 to go back.")
    username = input("Enter new username: ").strip()
    if username == "0":
        return None

    if not username:
        pr.error("Username cannot be empty.")
        return None

    if username in bank.users:
        pr.error("Username already exists.")
        return None

    password = pwinput.pwinput("Enter password: ").strip()
    if password == "0":
        return None

    if not password:
        pr.error("Password cannot be empty.")
        return None

    confirm_password = pwinput.pwinput("Confirm password: ").strip()
    if confirm_password == "0":
        return None

    if password != confirm_password:
        pr.error("Passwords do not match.")
        return None

    bank.create_user(username, password, True)
    pr.success(f"User {username} registered successfully!")
    return username


def main_menu(bank, username):
    while True:
        pr.header("\n--- Main Menu ---")
        pr.menu("1. Create Account")
        pr.menu("2. Deposit")
        pr.menu("3. Withdraw")
        pr.menu("4. Check Balance")
        pr.menu("5. Transfer Funds")
        pr.menu("6. My Accounts")
        pr.menu("7. Pay Bill")
        pr.menu("8. Logout")

        choice = input("Choose option (1-8): ")

        if choice == "1":
            pr.menu("Enter 0 to go back.")
            account_name = input("Enter account holder's name: ").strip()
            if account_name == "0":
                continue
            initial_balance = validate_positive_number(
                "Initial deposit amount (or 0 to cancel): ")
            if initial_balance == 0:
                pr.warning("Cancelled creating account.")
                continue
            bank.create_account(username, account_name, initial_balance)

        elif choice == "2":
            pr.menu("Enter 0 to go back.")
            acc_num = input("Enter account number: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number(
                    "Deposit amount (or 0 to cancel): ")
                if amount == 0:
                    pr.warning("Deposit cancelled.")
                    continue
                account.deposit(amount)
            else:
                pr.error("Account not found or access denied.")

        elif choice == "3":
            pr.menu("Enter 0 to go back.")
            acc_num = input("Enter account number: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number(
                    "Withdrawal amount (or 0 to cancel): ")
                if amount == 0:
                    pr.warning("Withdrawal cancelled.")
                    continue
                account.withdraw(amount)
            else:
                pr.error("Account not found or access denied.")

        elif choice == "4":
            pr.menu("Enter 0 to go back.")
            acc_num = input("Enter account number: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                account.check_balance()
            else:
                pr.error("Account not found or access denied.")

        elif choice == "5":
            pr.menu("Enter 0 to go back.")
            sender_acc = input("Your account number: ").strip()
            if sender_acc == "0":
                continue
            sender = bank.get_account(sender_acc)
            if sender and sender_acc in bank.get_user_accounts(username):
                recipient_acc = input("Recipient account number: ").strip()
                if recipient_acc == "0":
                    continue
                recipient = bank.get_account(recipient_acc)
                if recipient:
                    amount = validate_positive_number(
                        "Transfer amount (or 0 to cancel): ")
                    if amount == 0:
                        pr.warning("Transfer cancelled.")
                        continue
                    sender.transfer(amount, recipient, username, bank)
                else:
                    pr.error("Recipient account not found.")
            else:
                pr.error("Invalid sender account.")

        elif choice == "6":
            pr.header("\n--- Your Accounts ---")
            bank.list_user_accounts(username)

        elif choice == "7":
            pr.menu("Enter 0 to go back.")
            acc_num = input("Enter your account number: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if not account or acc_num not in bank.get_user_accounts(username):
                pr.error("Invalid account number or not your account.")
                continue

            pr.menu("Available companies: EC, CQ, FI")
            company = input("Enter company code (EC, CQ, FI): ").strip().upper()
            if company == "0":
                continue

            amount = validate_positive_number("Enter amount to pay: ")
            if amount == 0:
                pr.warning("Cancelled bill payment.")
                continue

            success = account.pay_bill(company, amount, bank, username)
            if success:
                # Optionally track session total if needed in-memory
                pass

        elif choice == "8":
            pr.warning("Logging out...")
            log_activity("User logout", username)
            break

        else:
            pr.error("Invalid choice.")


def main():
    bank = BankSystem()

    while True:
        choice = display_home_page()

        if choice == "exit":
            break
        elif choice == "login":
            username = login_page(bank)
            if username:
                main_menu(bank, username)
        elif choice == "register":
            username = register_page(bank)
            if username:
                main_menu(bank, username)


if __name__ == "__main__":
    main()
