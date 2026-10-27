
import json
import getpass
from pathlib import Path

VAULT_FILE = Path("vault.json")


def load_vault():
    """Load saved accounts from the JSON file."""
    if not VAULT_FILE.exists():
        return []

    try:
        with VAULT_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise ValueError(
            "vault.json contains invalid JSON. "
            "Back it up and repair it before continuing."
        ) from error

    if not isinstance(data, list):
        raise ValueError("The vault must contain a JSON list.")

    for account in data:
        if not isinstance(account, dict) or not all(
            isinstance(account.get(key), str)
            for key in ("website", "username", "password")
        ):
            raise ValueError("The vault contains an invalid account entry.")

    return data


def save_vault(accounts):
    """Save accounts to the JSON file."""
    with VAULT_FILE.open("w", encoding="utf-8") as file:
        json.dump(accounts, file, indent=4)


def add_account(accounts):
    website = input("Website or service: ").strip()
    username = input("Username or email: ").strip()

    if not website or not username:
        print("Website and username cannot be empty.")
        return

    password = getpass.getpass("Password (hidden while typing): ")

    if not password:
        print("Password cannot be empty.")
        return

    accounts.append({
        "website": website,
        "username": username,
        "password": password
    })

    save_vault(accounts)
    print("Account saved.")


def view_accounts(accounts):
    if not accounts:
        print("Your vault is empty.")
        return

    print("\n--- SAVED ACCOUNTS ---")

    for number, account in enumerate(accounts, start=1):
        print(f"{number}. Website: {account['website']}")
        print(f"   Username: {account['username']}")
        print("   Password: [hidden]")


def search_account(accounts):
    query = input("Search website: ").strip().casefold()

    if not query:
        print("Search cannot be empty.")
        return

    matches = [
        account for account in accounts
        if query in account["website"].casefold()
    ]

    if not matches:
        print("No matching accounts found.")
        return

    for account in matches:
        print(f"\nWebsite: {account['website']}")
        print(f"Username: {account['username']}")

        reveal = input("Reveal password? (y/n): ").strip().lower()
        if reveal == "y":
            print("Password:", account["password"])
        else:
            print("Password: [hidden]")


def delete_account(accounts):
    if not accounts:
        print("Your vault is empty.")
        return

    view_accounts(accounts)
    choice = input("Enter the account number to delete: ").strip()

    try:
        number = int(choice)
    except ValueError:
        print("Please enter a valid number.")
        return

    if number < 1 or number > len(accounts):
        print("Account number does not exist.")
        return

    removed = accounts[number - 1]
    confirm = input(
        f"Delete {removed['website']}? (y/n): "
    ).strip().lower()

    if confirm == "y":
        accounts.pop(number - 1)
        save_vault(accounts)
        print("Account deleted.")
    else:
        print("Deletion cancelled.")


def main():
    try:
        accounts = load_vault()
    except (ValueError, OSError) as error:
        print(f"Could not load the vault: {error}")
        print("No changes were made. Check the file before retrying.")
        return

    while True:
        print("\n========================")
        print("    PYTHON PASSWORD VAULT")
        print("========================")
        print("1. Add account")
        print("2. View accounts")
        print("3. Search account")
        print("4. Delete account")
        print("5. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_account(accounts)
            elif choice == "2":
                view_accounts(accounts)
            elif choice == "3":
                search_account(accounts)
            elif choice == "4":
                delete_account(accounts)
            elif choice == "5":
                print("Vault closed.")
                break
            else:
                print("Invalid choice. Enter 1-5.")

        except OSError as error:
            print(f"Could not save or read the file: {error}")


if __name__ == "__main__":
    main()
