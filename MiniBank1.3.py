# v1 first code
# v1.1 with some specifications
# v.1.2 hide passwords
# v.1.3 authomatic acount number example

import hashlib
import pwinput
from datetime import datetime


class BankAccount:
    def __init__(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance
        self.transaction_counter = 10000

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def check_balance(self):
        print(f"Current balance is €{self.balance:.2f}.")

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            recipient_account.balance += amount
            print(
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
            print("User not found.")
            return

        account_number = self._generate_account_number(account_name, initial_balance)
        new_account = BankAccount(account_number, account_name, initial_balance)
        self.accounts[account_number] = new_account
        self._add_user_account(username, account_number)
        print(f"Account created successfully!\nYour new account number: {account_number}")

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
            print("No accounts found.")
            return
        for acc_num in self.user_accounts[username]:
            account = self.accounts[acc_num]
            print(f"Account {acc_num}: {account.account_name} - €{account.balance:.2f}")

    def create_user(self, username, password):
        if username in self.users:
            print("Username already exists.")
            return
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        self.users[username] = hashed_pw
        print(f"User {username} created.")

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
                print("Amount must be positive.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number.")


def display_home_page():
    print("\n--- Welcome to Mini Bank ---")
    print("\n--- This was created for base for Master AAB Project ---")
    print("\n--- students for this project are: \nStudent: Fatmir Hasani - Frontend / Product Analyst\nStudent: Lendrit Berisha - Frontend / Product Analyst\nStudent: Majlind Avdylaj - Lead Programmer / Test\nStudent: Ertan Iliyaz - Backend programmer / Documentation\nMentor: Prof. Ass. Dr. Ramadan Dervishi (Product Owner)\n---")
    print("1. Login")
    print("2. Exit")
    while True:
        choice = input("Choose option (1-2): ")
        if choice == "1":
            return True
        elif choice == "2":
            print("Exiting application.")
            return False
        print("Invalid choice.")


def login_page(bank):
    print("\n--- Login ---")
    username = input("Username: ").strip()
    password = pwinput.pwinput("Password: ").strip()
    if bank.authenticate_user(username, password):
        print(f"Welcome {username}!")
        return username
    print("Invalid credentials.")
    return None


def main_menu(bank, username):
    while True:
        print("\n--- Main Menu ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Transfer Funds")
        print("6. My Accounts")
        print("7. Logout")

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
                print("Account not found or access denied.")

        elif choice == "3":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number("Withdrawal amount: ")
                account.withdraw(amount)
            else:
                print("Account not found or access denied.")

        elif choice == "4":
            acc_num = input("Enter account number: ").strip()
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                account.check_balance()
            else:
                print("Account not found or access denied.")

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
                    print("Recipient account not found.")
            else:
                print("Invalid sender account.")

        elif choice == "6":
            print("\n--- Your Accounts ---")
            bank.list_user_accounts(username)

        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid choice.")


def main():
    bank = BankSystem()
    bank.create_user("admin", "123")
    bank.create_user("user1", "123")

    while True:
        if not display_home_page():
            break

        username = None
        while not username:
            username = login_page(bank)

        main_menu(bank, username)


if __name__ == "__main__":
    main()
