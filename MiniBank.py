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
#
# v.1.9 Majlind
#   1. Validate transfers and withdrawals
#   2. Add transfers and accounts to json file
#   3. Add Integration testings
#   4. Add Pay Bills
#   5. Add Delete Account
# v.1.10 changed to Albanian Language | Lendrit changed - Majlind / Ertan reviewed code
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
    def _init_(self, account_number, account_name, balance=0):
        self.account_number = account_number
        self.account_name = account_name
        self.balance = balance
        self.transaction_counter = 10000

    def deposit(self, amount):
        self.balance += amount
        log_activity("Deposit", self.account_name,
                     f"Account: {self.account_number}, Amount: {amount}")
        pr.success(
            f"Deponuar €{amount:.2f}. Balanca e re eshte €{self.balance:.2f}.")

    def withdraw(self, amount):
        if amount > self.balance:
            pr.error("Nuk ka mjete te mjaftueshme.")
        elif amount > 500:
            # duhet me u bo brenda sessionit
            pr.error("Eshte arritur limiti maksimal prej 500€.")
        else:
            self.balance -= amount
            log_activity("Withdraw", self.account_name,
                         f"Account: {self.account_number}, Amount: {amount}")
            pr.success(
                f"Shuma e terhequr €{amount:.2f}. Balanci i ri eshte €{self.balance:.2f}.")

    def check_balance(self):
        pr.success(f"Balanci aktual eshte €{self.balance:.2f}.")

    def transfer(self, amount, recipient_account, sender_username, bank_system):
        if amount > self.balance:
            pr.error("Nuk ka mjete te mjaftueshme.")
        elif amount > 1000:
            pr.error("Eshte arritur transferi maksimal prej 1000€.")
        else:
            self.balance -= amount
            recipient_account.balance += amount
            log_activity("Transfer", self.account_name,
                         f"From: {self.account_number}, To: {recipient_account.account_number}, Amount: {amount}")
            pr.success(
                f"Shuma e transferuar €{amount:.2f} ne llogarine {recipient_account.account_number}. Balanci i ri eshte €{self.balance:.2f}.")
            # Save transfer to JSON
            transfer_data = {
                "from": self.account_number,
                "to": recipient_account.account_number,
                "amount": amount,
                "timestamp": datetime.now().isoformat()
            }
            bank_system.users[sender_username]["transfers"].append(
                transfer_data)
            bank_system.save_users_to_file()

    def pay_bill(self, company, amount, bank_system, username):
        allowed_companies = {
            "EC": "The Bright Light Electric Company (EC)",
            "CQ": "Credit Card Company Q (CQ)",
            "FI": "Fast Internet, Inc. (FI)"
        }

        if company not in allowed_companies:
            pr.error("Kompani e pa njohur. Duhet te jete EC, CQ, ose FI.")
            return False

        if amount > 2000:
            pr.error("Nuk mund te paguani me shume se shuma €2000 ne nje sesion.")
            return False

        if self.balance - amount < 0:
            pr.error("Nuk ka mjete te mjaftueshme per te paguar faturen.")
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
            f"Me sukses eshte paguar shuma prej €{amount:.2f} ne {allowed_companies[company]}. Balanci i ri: €{self.balance:.2f}")
        return True


class BankSystem:
    def _init_(self):
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
        name_part = account_name.upper().replace(" ", "")[:20].ljust(20, "")
        acc_num = f"{self.account_counter:05d}"
        self.account_counter += 1
        amount = f"{int(initial_balance * 100):08d}"
        mm = f"{datetime.now().month:02d}"
        return f"{cc}{name_part}{acc_num}{amount}{mm}"

    def create_account(self, username, account_name, initial_balance=0, save=True):
        if username not in self.users:
            pr.warning("Useri nuk eshte gjetur.")
            return

        # Check if the user already has an account with the same name
        for acc_num in self.get_user_accounts(username):
            acc = self.accounts.get(acc_num)
            if acc and acc.account_name.lower() == account_name.lower():
                pr.error("Kjo llogari eshte ekzistuese.")
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
            f"Llogaria juaj eshte krijuar me sukses!\nNumri i llogarise suaj eshte: {account_number}")

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
            pr.warning("Nuk ka llogari ekzistuese.")
            return
        for acc_num in self.user_accounts[username]:
            account = self.accounts[acc_num]
            pr.success(
                f"Llogaria {acc_num}: {account.account_name} - €{account.balance:.2f}")

    def create_user(self, username, password, save):
        if not username or not password:
            pr.error(
                "Emri i perdoruesit dhe fjalekalimi nuk duhet te jene te zbasura.")
            return
        if username in self.users:
            pr.error("Emri i perdoruesit eshte ekzistues.")
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
        pr.success(f"Perdoruesi {username} eshte krijuar me sukses.")

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save_users_to_file()

    def authenticate_user(self, username, password):
        if username in self.users:
            hashed_pw = hashlib.sha256(password.encode()).hexdigest()
            return self.users[username]["password"] == hashed_pw
        return False

    def delete_account(self, username, account_number):
        if username not in self.users:
            pr.error("Perdoruesi nuk ekziston.")
            return

        # Find and remove account from user's account list
        user_accounts = self.users[username].get("accounts", [])
        updated_accounts = [
            acc for acc in user_accounts if acc["account_number"] != account_number]

        if len(user_accounts) == len(updated_accounts):
            pr.error("Numri i llogarise nuk eshte gjendur ne llogarine tuaj.")
            return

        self.users[username]["accounts"] = updated_accounts

        # Remove from self.accounts
        if account_number in self.accounts:
            del self.accounts[account_number]

        # Remove from self.user_accounts
        if username in self.user_accounts:
            self.user_accounts[username] = [
                acc_num for acc_num in self.user_accounts[username] if acc_num != account_number
            ]

        self.save_users_to_file()
        log_activity("Account deleted", username,
                     f"Account Number: {account_number}")
        pr.success(f"Llogaria {account_number} eshte fshire me sukses.")


def validate_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                pr.error("Shuma duhet te jete pozitive.")
                continue
            return value
        except ValueError:
            pr.error("Vlera jo valide. Ju lutem shtypni nje numer.")


def display_home_page():
    pr.header("\n--- Mireservini ne Mini Bank ---")
    pr.header("\n--- Ky projekt eshte krijuar per fakulltetin Master - AAB ---")
    pr.header("\n--- Studentet pjesemarres ne projekt jane: \nStudenti: Fatmir Hasani - Frontend / Product Analyst\nStudenti: Lendrit Berisha - Frontend / Product Analyst\nStudenti: Majlind Avdylaj - Lead Programmer / Test\nStudenti: Ertan Iliyaz - Backend programmer / Documentation\nMentor: Prof. Ass. Dr. Ramadan Dervishi (Product Owner)\n---")
    pr.menu("1. Kycu")
    pr.menu("2. Regjistrohu")
    pr.menu("3. Dil")

    while True:
        choice = input("Zgjedhni nje opsion (1-3): ")

        if choice == "1":
            return "login"
        elif choice == "2":
            return "register"
        elif choice == "3":
            pr.warning("Duke dalur nga aplikacioni.")
            log_activity("Application exit")
            return "exit"
        pr.error("Zgjedhje invalide.")


def login_page(bank):
    pr.header("\n--- Kycu ---")
    pr.menu("Klikoni 0 per te shkuar mbrapa.")
    username = input("Emri perdoruesit: ").strip()
    if username == "0":
        return None

    password = pwinput.pwinput("Fjalekalimi: ").strip()
    if password == "0":
        return None

    if bank.authenticate_user(username, password):
        pr.success(f"Mireservini {username}!")
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
    pr.error("Kredencialet gabim.")
    return None


def register_page(bank):
    pr.header("\n--- Regjistrohu ---")
    pr.menu("Klikoni 0 per te shkuar mbrapa.")
    username = input("Shkruani nje emer perdoruesi: ").strip()
    if username == "0":
        return None

    if not username:
        pr.error("Emri i perdoruesit nuk duhet te jete i zbrasur.")
        return None

    if username in bank.users:
        pr.error("Ky emer perdoruesi ekziston.")
        return None

    password = pwinput.pwinput("Shkruani fjalekalimin: ").strip()
    if password == "0":
        return None

    if not password:
        pr.error("Fjalekalimi nuk duhet te jete i zbrasur.")
        return None

    confirm_password = pwinput.pwinput("Fjalekalimi u konfirmua: ").strip()
    if confirm_password == "0":
        return None

    if password != confirm_password:
        pr.error("Fjalekalimet nuk pershtaten.")
        return None

    bank.create_user(username, password, True)
    pr.success(f"Useri {username} eshte regjistruar me sukses!")
    return username


def main_menu(bank, username):
    while True:
        pr.header("\n--- Menu kryesore ---")
        pr.menu("1. Krijoni llogari")
        pr.menu("2. Deponim")
        pr.menu("3. Terheqje")
        pr.menu("4. Kontrolloni balancen")
        pr.menu("5. Transferimi i fondeve")
        pr.menu("6. Llogaria ime")
        pr.menu("7. Paguaj faturen")
        pr.menu("8. Fshije llogarine")
        pr.menu("9. Shkycu")

        choice = input("Zgjedhni opsionin (1-8): ")

        if choice == "1":
            pr.menu("Klikoni 0 per te shkruar mbrapa.")
            account_name = input(
                "Vendosni emrin e mbajtësit të llogarisë: ").strip()
            if account_name == "0":
                continue
            initial_balance = validate_positive_number(
                "Shkruani shumen per te deponuar (ose 0 per te anuluar): ")
            if initial_balance == 0:
                pr.warning("Krijimi i llogarise u anulua.")
                continue
            bank.create_account(username, account_name, initial_balance)

        elif choice == "2":
            pr.menu("Klikoni 0 per te shkruar mbrapa.")
            acc_num = input("Shkruani numrin e llogarise: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number(
                    "Shuma e deponuar (ose 0 per anulim): ")
                if amount == 0:
                    pr.warning("Deponimi u anulua.")
                    continue
                account.deposit(amount)
            else:
                pr.error("Llogaria nuk u gjet ose qasja u refuzua.")

        elif choice == "3":
            pr.menu("Klikoni 0 per te shkruar mbrapa.")
            acc_num = input("Shkruani numrin e llogarise: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                amount = validate_positive_number(
                    "Shuma per terheqje (or 0 to cancel): ")
                if amount == 0:
                    pr.warning("Terheqja u anulua.")
                    continue
                account.withdraw(amount)
            else:
                pr.error("Llogaria nuk u gjet ose qasja u refuzua.")

        elif choice == "4":
            pr.menu("Klikoni 0 per te shkruar mbrapa.")
            acc_num = input("Shkruani numrin e llogarise: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if account and acc_num in bank.get_user_accounts(username):
                account.check_balance()
            else:
                pr.error("Llogaria nuk u gjet ose qasja u refuzua.")

        elif choice == "5":
            pr.menu("Klikoni 0 per te shkruar mbrapa.")
            sender_acc = input("Numri i llogarise: ").strip()
            if sender_acc == "0":
                continue
            sender = bank.get_account(sender_acc)
            if sender and sender_acc in bank.get_user_accounts(username):
                recipient_acc = input(
                    "Numri i llogarise se marresit: ").strip()
                if recipient_acc == "0":
                    continue
                recipient = bank.get_account(recipient_acc)
                if recipient:
                    amount = validate_positive_number(
                        "Shuma per transfer (ose 0 per anulim): ")
                    if amount == 0:
                        pr.warning("Transferi u anulua.")
                        continue
                    sender.transfer(amount, recipient, username, bank)
                else:
                    pr.error("Llogaria e marresit nuk u gjend.")
            else:
                pr.error("Llogaria e derguesit nuk u gjend.")

        elif choice == "6":
            pr.header("\n--- Llogaria juaj ---")
            bank.list_user_accounts(username)

        elif choice == "7":
            pr.menu("Klikoni 0 per t'u kthyer mbrapa.")
            acc_num = input("Shkruani numrin e llogarise suaj: ").strip()
            if acc_num == "0":
                continue
            account = bank.get_account(acc_num)
            if not account or acc_num not in bank.get_user_accounts(username):
                pr.error("Llogaria nuk u gjet ose qasja u refuzua.")
                continue

            pr.menu("Kompanite e disponueshme: EC, CQ, FI")
            company = input(
                "Shkruani kodin e kompanise (EC, CQ, FI): ").strip().upper()
            if company == "0":
                continue

            amount = validate_positive_number(
                "Shkruani shumen per te paguar: ")
            if amount == 0:
                pr.warning("Pagesa e fatures u anulua.")
                continue

            success = account.pay_bill(company, amount, bank, username)
            if success:
                pass
        elif choice == "8":
            pr.header("\n--- Llogaria juaj ---")
            bank.list_user_accounts(username)
            pr.menu("Shkruani 0 per t'u kthyer mbrapa.")
            acc_num = input(
                "Shkruani numrin e llogarise per ta fshire: ").strip()
            if acc_num == "0":
                continue
            if acc_num not in bank.get_user_accounts(username):
                pr.error("Llogaria nuk u gjet ose qasja u refuzua.")
                continue
            bank.delete_account(username, acc_num)

        elif choice == "9":
            pr.warning("Duke u shkyqur...")
            log_activity("Perdoruesi u shkyc", username)
            break

        else:
            pr.error("Zgjedhje e gabuar.")


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
