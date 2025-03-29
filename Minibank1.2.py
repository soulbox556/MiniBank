# v1 first code
# v1.1 with some specifications
# v.1.2 hide passswords
# v.1.3 will add authomatic acount number example
import hashlib
import getpass


class BankAccount:
    def __init__(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited €{amount:.2f}. New balance is €{self.balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(
                f"Withdrew €{amount:.2f}. New balance is €{self.balance:.2f}.")

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
        self.user_accounts = {}  # Maps users to their accounts

    def create_account(self, username, account_number, account_name, initial_balance=0):
        if account_number in self.accounts:
            print("Account number already exists.")
            return
        if username not in self.users:
            print("User not found.")
            return

        new_account = BankAccount(
            account_number, account_name, initial_balance)
        self.accounts[account_number] = new_account
        self._add_user_account(username, account_number)
        print(f"Account {account_number} created for {account_name}.")

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
            print(
                f"Account {acc_num}: {account.account_name} - €{account.balance:.2f}")

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

    # Use getpass to hide password input with '*'
    password = getpass.getpass("Password: ").strip()

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
            account_number = input("Enter new account number: ").strip()
            account_name = input("Enter account name: ").strip()
            initial_balance = validate_positive_number(
                "Initial deposit amount: ")
            bank.create_account(username, account_number,
                                account_name, initial_balance)

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

    # Create sample users
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
