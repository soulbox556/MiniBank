class BankAccount:
    def __init__(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance
# €€€€€€
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited €{amount}. New balance is €{self.balance}.")

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print(f"Withdrew €{amount}. New balance is €{self.balance}.")

    def check_balance(self):
        print(f"Current balance is €{self.balance}.")

    def transfer(self, amount, recipient_account):
        if amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            recipient_account.balance += amount
            print(
                f"Transferred €{amount} to account {recipient_account.account_number}. New balance is €{self.balance}.")


class BankSystem:
    def __init__(self):
        self.accounts = {}
        self.users = {}

    def create_account(self, account_number, account_name, initial_balance=0):
        if account_number in self.accounts:
            print("Account number already exists.")
        else:
            new_account = BankAccount(
                account_number, account_name, initial_balance)
            self.accounts[account_number] = new_account
            print(f"Account {account_number} created for {account_name}.")

    def get_account(self, account_number):
        return self.accounts.get(account_number)

    def list_accounts(self):
        for account in self.accounts.values():
            print(
                f"Account Number: {account.account_number}, Name: {account.account_name}, Balance: €{account.balance}")

    def create_user(self, username, password):
        if username in self.users:
            print("Username already exists.")
        else:
            self.users[username] = password
            print(f"User {username} created.")

    def authenticate_user(self, username, password):
        if username in self.users and self.users[username] == password:
            return True
        else:
            return False


def display_home_page():
    print("\n--- Welcome to Mini Bank ---")
    print("-------------------------------")
    print("A simple banking system for managing accounts.")
    print("-------------------------------")
    print("1. Proceed to Login")
    print("2. Exit Application")

    choice = input("Choose an option: ")

    if choice == "1":
        return True
    elif choice == "2":
        print("Exiting the application.")
        return False
    else:
        print("Invalid choice. Please choose a valid option.")
        return display_home_page()


def login_page(bank):
    print("\n--- Login Page ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if bank.authenticate_user(username, password):
        print("Login successful!")
        return username
    else:
        print("Invalid username or password. Please try again.")
        return login_page(bank)


def main():
    bank = BankSystem()

    # Pre-register some users for demonstration
    bank.create_user("admin", "123123")
    bank.create_user("user1", "pass123")

    if display_home_page():
        username = login_page(bank)

        while True:
            print("\n--- Mini Bank Console ---")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Check Balance")
            print("5. Transfer Funds")
            print("6. List Accounts")
            print("7. Exit")

            choice = input("Choose an option: ")

            if choice == "1":
                account_number = input("Enter account number: ")
                account_name = input("Enter account name: ")
                initial_balance = float(
                    input("Enter initial balance (default=0): ") or 0)
                bank.create_account(
                    account_number, account_name, initial_balance)

            elif choice == "2":
                account_number = input("Enter account number: ")
                account = bank.get_account(account_number)
                if account:
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                else:
                    print("Account not found.")

            elif choice == "3":
                account_number = input("Enter account number: ")
                account = bank.get_account(account_number)
                if account:
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                else:
                    print("Account not found.")

            elif choice == "4":
                account_number = input("Enter account number: ")
                account = bank.get_account(account_number)
                if account:
                    account.check_balance()
                else:
                    print("Account not found.")

            elif choice == "5":
                sender_account_number = input(
                    "Enter sender's account number: ")
                sender_account = bank.get_account(sender_account_number)
                if sender_account:
                    recipient_account_number = input(
                        "Enter recipient's account number: ")
                    recipient_account = bank.get_account(
                        recipient_account_number)
                    if recipient_account:
                        amount = float(input("Enter amount to transfer: "))
                        sender_account.transfer(amount, recipient_account)
                    else:
                        print("Recipient account not found.")
                else:
                    print("Sender account not found.")

            elif choice == "6":
                bank.list_accounts()

            elif choice == "7":
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
