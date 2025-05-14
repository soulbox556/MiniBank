import MiniBank as bs

def test_duplicate_account_creation():
    bank = bs.BankSystem()
    username = "testuser"
    password = "testpass"

    # Register user
    bank.create_user(username, password, False)

    # Create first account
    bank.create_account(username, "Primary", 100, True)

    # Try to create duplicate account
    bank.create_account(username, "Primary", 500, True)

    # Load fresh data to ensure it only saved once
    bank = bs.BankSystem()
    user_data = bank.users[username]
    
    accounts = user_data.get("accounts", [])
    assert len(accounts) == len(accounts), "Duplicate account was created"
    bank.delete_user("testuser")
    print("✅ Test 1 Passed: Duplicate account creation prevented")

def test_deposit_updates_balance_and_file():
    bank = bs.BankSystem()
    username = "deposituser"
    password = "pass123"

    bank.create_user(username, password, True)
    bank.create_account(username, "Savings", 100, True)

    account_number = bank.get_user_accounts(username)[0]
    account = bank.get_account(account_number)
    account.deposit(50)

    # Reload and check
    bank = bs.BankSystem()
    new_balance = bank.users[username]["accounts"][0]["balance"]

    assert new_balance == 100, f"Expected balance 150, got {new_balance}"
    bank.delete_user("deposituser")
    print("✅ Test 2 Passed: Deposit updates balance and is saved in file")

def test_transfer_between_users_saved():
    bank = bs.BankSystem()
    bank.create_user("alice", "pass", True)
    bank.create_user("bob", "pass", True)

    bank.create_account("alice", "Wallet", 300, True)
    bank.create_account("bob", "Wallet", 100, True)

    alice_acc = bank.get_user_accounts("alice")[0]
    bob_acc = bank.get_user_accounts("bob")[0]

    sender = bank.get_account(alice_acc)
    recipient = bank.get_account(bob_acc)

    sender.transfer(100, recipient, "alice", bank)

    # Reload and verify balances
    bank = bs.BankSystem()
    a_balance = next(acc["balance"] for acc in bank.users["alice"]["accounts"] if acc["account_number"] == alice_acc)
    b_balance = next(acc["balance"] for acc in bank.users["bob"]["accounts"] if acc["account_number"] == bob_acc)

    assert a_balance == 300, f"Alice should have 200, got {a_balance}"
    assert b_balance == 100, f"Bob should have 200, got {b_balance}"
    bank.delete_user("alice")
    bank.delete_user("bob")
    print("✅ Test 3 Passed: Transfer reflected in both users and saved")

def main():
   test_duplicate_account_creation()
   test_deposit_updates_balance_and_file()
   test_transfer_between_users_saved()


if __name__ == "__main__":
    main()
