import json
import random
import os
from datetime import datetime

# Constants
JSON_DIR = "./json"
TRANSACTION_DIR = f"{JSON_DIR}/transactions"  # transaction files are lists
USER_DATA_FILE = f"{JSON_DIR}/user_data.json"  # user data file is dict
SPECIAL_CHARACTERS = "!@#$%^&*()"


# helper functions
def clear_screen():
    """
    Clears the terminal screen.
    """

    os.system("cls" if os.name == "nt" else "clear")


def load_data(file_name):
    """
    Load data from JSON file. If the file doesn't exist, return an empty dictionary.

    @param: file_name (str): name of the file to load data from
    @return: data (dict or list): data from the files
    """

    # if the file do not exist, create with empty data
    if not os.path.exists(file_name):
        if file_name == USER_DATA_FILE:
            save_data({}, file_name)  # dict for user_data.json
        else:
            save_data([], file_name)  # list for transaction files

    # if the file exists, load the data from the file
    with open(file_name, "r") as file:
        return json.load(file)


def save_data(data_to_save, file_name):
    """
    Save data to a JSON file.

    @param: data (dict): data to save to the file
    @param: file_name (str): name of the file to save the data to
    """

    try:
        with open(file_name, "w") as file:
            json.dump(data_to_save, file)
    except IOError as e:
        print(f"Error saving data: {e}")
    return


def generate_account_number(user_data):
    """
    Generate a unique account number for a new user (5 random digits).

    @param: user_data (dict): dictionary of existing users
    @return: account_number (str): unique account number for the new user
    """

    while True:
        account_number = str(random.randint(10000, 99999))

        # check if the account number is unique
        if not any(
            user["account_number"] == account_number for user in user_data.values()
        ):
            return account_number


def is_password_valid(password):
    """
    Check password validity.

    @param: password (str): password to check
    @return: errors (list): list of errors if the password is invalid
    """

    errors = []
    if len(password) < 7:
        errors.append("Password must be at least 7 characters long.")
    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")
    if not any(char in SPECIAL_CHARACTERS for char in password):
        errors.append("Password must contain at least one special character.")
    return errors


def is_pin_valid(pin):
    """
    Check PIN validity (must be 4 digits).

    @param: pin (str): PIN to check
    @return: valid (bool): True if the PIN is valid, False otherwise
    """

    return len(pin) == 4 and pin.isdigit()


def log_transaction(username, transaction):
    """
    Log a transaction in the user's individual transaction file.

    @param: username (str): username of the user
    @param: transaction (dict): transaction to log
    """

    # load the transaction file
    transaction_file = f"{TRANSACTION_DIR}/{username}.json"
    transactions = load_data(transaction_file)

    # insert the transaction at the beginning of the list and save the file
    transactions.insert(0, transaction)
    save_data(transactions, transaction_file)


def validate_amount(amount_str):
    """
    Validate and convert amount input.
    """

    # check if the amount is a valid number and greater than 0
    try:
        amount = float(amount_str)
        if amount <= 0:
            return False, "Amount must be greater than 0."
        return True, amount
    except ValueError:
        return False, "Invalid amount format."


# user functions
def register_user(user_data):
    """
    Register a new user and create their transaction file.

    @param: user_data (dict): dictionary of existing users
    """

    clear_screen()

    # get username and check if it is already taken
    print("\nRegister a new user:")
    username = input("Enter username: ")
    if username in user_data:
        print("Error: Username already exists.")
        input("\nPress Enter to return to the menu.")
        return

    # get password and validate it
    password = input("Enter login password: ")
    if len(errors := is_password_valid(password)):
        print("Invalid password:")
        for error in errors:
            print(f"- {error}")
        return input("\nPress Enter to return to the menu.")

    # get PIN and validate it
    pin = input("Enter a 4-digit PIN: ")
    if not is_pin_valid(pin):
        print("Error: PIN must be a 4-digit number.")
        return input("\nPress Enter to return to the menu.")

    # generate a unique account number for the new user
    account_number = generate_account_number(user_data)

    # create a new user in the user_data dictionary and save it to user_data file
    user_data[username] = {
        "username": username,
        "password": password,
        "pin": pin,
        "account_number": account_number,
        "balance": 100,
    }
    save_data(user_data, USER_DATA_FILE)

    # create an empty transaction file for the new user
    save_data([], f"{TRANSACTION_DIR}/{username}.json")

    print(f"Registration successful! Your account number is {account_number}.")
    input("\nPress Enter to return to the menu.")


def login_user(user_data):
    """
    Log in an existing user.
    """

    clear_screen()

    print("\nLogin:")
    username = input("Enter username: ")
    password = input("Enter password: ")

    # check if the username is in the user_data dictionary and the password is corrects
    if username not in user_data or user_data[username]["password"] != password:
        print("Error: Invalid username or password.")
        input("\nPress Enter to return to the menu.")
        return None
    return username


# Financial Operation Functions
def show_history(username):
    """
    Show the transaction history for a user.
    """

    clear_screen()

    # load the transaction file
    transaction_file = f"{TRANSACTION_DIR}/{username}.json"
    transactions = load_data(transaction_file)

    # print the transaction history
    print("\n--- Transaction History ---\n")
    if not transactions:
        print("No transactions found.")
        return input("\nPress Enter to return to the menu.")

    for transaction in transactions:
        if transaction["type"] == "Transfer":
            print(f"[{transaction['time']}]\n")
            print(f"- Type: {transaction['type']}")
            print(f"- From: {transaction['from']}")
            print(f"- To: {transaction['to']}")
            print(f"- Amount: ${transaction['amount']}")
        else:
            print(f"[{transaction['time']}]\n")
            print(f"- Type: {transaction['type']}")
            print(f"- Amount: ${transaction['amount']}")
        print("-" * 50)
    return input("\nPress Enter to return to the menu.")


def withdraw(user_data, username):
    """
    Withdraw money for the logged-in user.
    """

    clear_screen()

    # get the user from the user_data dictionary
    user = user_data[username]
    print("\nWithdraw Money:")

    # get the amount and validate it
    amount_str = input("Enter amount to withdraw: ")
    valid, result = validate_amount(amount_str)
    if not valid:
        return input(f"Error: {result}. Press Enter to return to the menu.")
    amount = result

    # check if the amount is greater than the user's balance
    if amount > user["balance"]:
        return input("Error: Insufficient balance. Press Enter to return to the menu.")

    # get the PIN and check if it is correct
    pin = input("Enter PIN: ")
    if pin != user["pin"]:
        return input("Error: Incorrect PIN. Press Enter to return to the menu.")

    # deduct the amount from the user's balance
    user["balance"] -= amount

    # log the transaction in the transaction file
    log_transaction(
        username,
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Withdraw",
            "amount": amount,
        },
    )
    save_data(user_data, USER_DATA_FILE)
    print(f"Withdrawal successful. New balance: ${user['balance']}")
    input("\nPress Enter to return to the menu.")
    return


def deposit(user_data, username):
    """
    Deposit money for the logged-in user.
    """

    clear_screen()
    # get the user from the user_data dictionary
    user = user_data[username]
    print("\nDeposit Money:")

    # get the amount and validate it
    amount_str = input("Enter amount to deposit: ")
    valid, result = validate_amount(amount_str)
    if not valid:
        return input(f"Error: {result}. Press Enter to return to the menu.")
    amount = result

    # get the PIN and check if it is correct
    pin = input("Enter PIN: ")
    if pin != user["pin"]:
        return input("Error: Incorrect PIN. Press Enter to return to the menu.")

    # add the amount to the user's balance
    user["balance"] += amount

    # log the transaction in the transaction file
    log_transaction(
        username,
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Deposit",
            "amount": amount,
        },
    )
    save_data(user_data, USER_DATA_FILE)
    print(f"Deposit successful. New balance: ${user['balance']}")
    input("\nPress Enter to return to the menu.")


def transfer(user_data, username):
    """
    Transfer money to another user.
    """

    clear_screen()
    # get the user from the user_data dictionary
    user = user_data[username]
    print("\nTransfer Money:")

    # get the recipient's account number
    account_number = input("Enter recipient's account number: ")

    # find the recipient by account number
    recipient = next(
        (
            user
            for user in user_data.values()
            if user["account_number"] == account_number
        ),
        None,
    )

    # check if the recipient is found and is not the same as the sender
    if not recipient:
        return input(
            "Error: Recipient account not found. Press Enter to return to the menu."
        )

    if account_number == user["account_number"]:
        return input(
            "Error: You cannot transfer money to your own account. Press Enter to return to the menu."
        )

    # get the amount and validate it
    amount_str = input("Enter amount to transfer: ")
    valid, result = validate_amount(amount_str)
    if not valid:
        return input(f"Error: {result}. Press Enter to return to the menu.")
    amount = result

    # check if the amount is greater than the user's balance
    if amount > user["balance"]:
        return input("Error: Insufficient balance. Press Enter to return to the menu.")

    # get the PIN and check if it is correct
    pin = input("Enter PIN: ")
    if pin != user["pin"]:
        return input("Error: Incorrect PIN. Press Enter to return to the menu.")

    # Deduct from sender and add to recipient
    user["balance"] -= amount
    recipient["balance"] += amount

    # Log transactions for both sender and recipient to their transaction files
    log_transaction(
        username,
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Transfer",
            "from": username,
            "to": recipient["username"],
            "amount": amount,
        },
    )
    log_transaction(
        recipient["username"],
        {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "Transfer",
            "from": username,
            "to": recipient["username"],
            "amount": amount,
        },
    )
    save_data(user_data, USER_DATA_FILE)
    print(f"Transfer successful. New balance: ${user['balance']}")
    input("\nPress Enter to return to the menu.")


def main_screen(data, username):
    """
    Main screen for a logged-in user.
    """

    # get the user from the user_data dictionary
    user = data[username]

    # show the main menu
    while True:
        try:
            clear_screen()
            print("=== Main Menu ===")
            print(f"Welcome, {username}")
            print(f"Account: {user['account_number']}")
            print(f"Balance: ${user['balance']:.2f}")
            print("\nOptions:")
            print("1. View Transaction History")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Transfer Money")
            print("5. Logout")

            # get the choice and validate it
            choice = input("\nChoose an option (1-5): ").strip()
            if choice == "1":
                show_history(username)
            elif choice == "2":
                withdraw(data, username)
            elif choice == "3":
                deposit(data, username)
            elif choice == "4":
                transfer(data, username)
            elif choice == "5":
                input(
                    "Successfully logged out. Press Enter to return to the initial menu."
                )
                return
            else:
                input("Invalid option. Please press Enter to try again.")
                continue

        except Exception as e:
            print(f"An error occurred: {e}")
            input("\nPress Enter to return to the menu.")
            continue


def init_screen():
    """
    Initial screen.
    """

    while True:
        clear_screen()
        user_data = load_data(USER_DATA_FILE)
        print("\n=== PL Banking System ===")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("\nChoose an option (1-3): ").strip()

        # define the actions for each choice and execute them
        if choice == "1":
            register_user(user_data)
        elif choice == "2":
            username = login_user(user_data)
            if username:
                main_screen(user_data, username)
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            input("Invalid option. Please press Enter to try again.")


# execute the program when the file is run
if __name__ == "__main__":
    # ensure the necessary directories exist
    os.makedirs(JSON_DIR, exist_ok=True)
    os.makedirs(TRANSACTION_DIR, exist_ok=True)

    # run the main program
    init_screen()
