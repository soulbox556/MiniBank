# v1 first code
# v1.1 with some specifications
# v.1.2 hide passwords
# v.1.3 authomatic acount number example
# v.1.4 Eshte finalizuar fajli dhe tani do te punohet permes github : EI MA

import hashlib
import pwinput
from datetime import datetime
import AppPrints as pr

class BankAccount:
    def __init__(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance
        self.transaction_counter = 10000

    def deposit(self, amount):
        self.balance += amount
        pr.success(f"Deposited €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.balance:
            pr.error("Insufficient funds.")
        else:
            self.balance -= amount
            pr.success(f"Withdrew €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def check_balance(self):
        pr.success(f"Current balance is €{self.balance:.2f}.")

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            pr.error("Insufficient funds.")
        else:
            self.balance -= amount
            recipient_account.balance += amount
            pr.success(
                f"Transferred €{amount:.2f} to account {recipient_account.account_number}. New balance is €{self.balance:.2f}.")


class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.users = {}
        self.user_accounts = {}
        self.account_counter = 10000

    def _generate_account_number(self, account_name, initial_balance):
        cc = "05"
        name_part = account_name.upper().replace(" ", "_")[:20].ljust(20, "_")
        acc_num = f"{self.account_counter:05d}"
        self.account_counter += 1
        amount = f"{int(initial_balance * 100):08d}"
        mm = f"{datetime.now().month:02d}"
        return f"{cc}_{name_part}_{acc_num}_{amount}_{mm}"

    def create_account(self, username, account_name, initial_balance=0):
        if username not in self.users:
            pr.warning("User not found.")
            return

        account_number = self._generate_account_number(account_name, initial_balance)
        new_account = BankAccount(account_number, account_name, initial_balance)
        self.accounts[account_number] = new_account
        self._add_user_account(username, account_number)
        pr.success(f"Account created successfully!\nYour new account number: {account_number}")

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
            pr.success(f"Account {acc_num}: {account.account_name} - €{account.balance:.2f}")

    def create_user(self, username, password):
        if username in self.users:
            pr.error("Username already exists.")
            return
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_pw
        pr.success(f"User {username} created.")

    def authenticate_user(self, username, password):
        if username in self.users:
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            return self.users[username] == hashed_pw
        return False


def validate_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
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
    pr.menu("2. Exit")
    while True:
        choice = input("Choose option (1-2): ")
        if choice == "1":
            return True
        elif choice == "2":
            pr.warning("Exiting application.")
            return False
        pr.error("Invalid choice.")


def login_page(bank):
    pr.header("\n--- Login ---")
    username = input("Username: ").strip()
    password = pwinput.pwinput("Password: ").strip()
    if bank.authenticate_user(username, password):
        pr.success(f"Welcome {username}!")
        return username
    pr.error("Invalid credentials.")
    return None


def main_menu(bank, username):
    while True:
        pr.header("\n--- Main Menu ---")
        pr.menu("1. Create Account")
        pr.menu("2. Deposit")
        pr.menu("3. Withdraw")
        pr.menu("4. Check Balance")
        pr.menu("5. Transfer Funds")
        pr.menu("6. My Accounts")
        pr.menu("7. Logout")

        choice = input("Choose option (1-7): ")

        if choice == "1":
            account_name = input("Enter account holder's name: ").strip()
            initial_balance = validate_positive_number("Initial deposit amount: ")
            bank.create_account(username, account_name, initial_balance)

        elif choice == "2":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number("Deposit amount: ")
                account.deposit(amount)
            else:
                pr.error("Account not found or access denied.")

        elif choice == "3":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number("Withdrawal amount: ")
                account.withdraw(amount)
            else:
                pr.error("Account not found or access denied.")

        elif choice == "4":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                account.check_balance()
            else:
                pr.error("Account not found or access denied.")

        elif choice == "5":
            sender_acc = input("Your account number: ").strip()
            sender = bank.get_account(sender_acc)
            if sender and sender_acc in bank.get_user_accounts(username):
                recipient_acc = input("Recipient account number: ").strip()
                recipient = bank.get_account(recipient_acc)
                if recipient:
                    amount = validate_positive_number("Transfer amount: ")
                    sender.transfer(amount, recipient)
                else:
                    pr.error("Recipient account not found.")
            else:
                pr.error("Invalid sender account.")

        elif choice == "6":
            pr.header("\n--- Your Accounts ---")
            bank.list_user_accounts(username)

        elif choice == "7":
            pr.warning("Logging out...")
            break

        else:
            pr.error("Invalid choice.")


def main():
    bank = BankSystem()
    bank.create_user("admin", "123")
    bank.create_user("user1", "123")
    bank.create_user("user2", "123")

    while True:
        if not display_home_page():
            break

        username = None
        while not username:
            username = login_page(bank)

        main_menu(bank, username)


if __name__ == "__main__":
    main()
