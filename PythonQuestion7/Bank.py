import json
import sys
import os.path


class Bank:
    ledger_file_path = "Ledger.txt"

    @staticmethod
    def get_records():
        """The function gets the record fro, the ledger file and if the file doesn't exists it creates a new file"""
        records = []
        # First check that the file exists - if it doesn't lets create a new one
        if not os.path.isfile(Bank.ledger_file_path):
            # Create a new file for the bank's ledger
            temp_file = open(Bank.ledger_file_path, "w+")
        # Now the ledger exists for sure so we need to read from it
        ledger_file = open(Bank.ledger_file_path, "r")
        # If the ledger is empty we don't have any records yet so we return an empty record list
        if len(ledger_file.readlines()) == 0:
            print("Empty")
            ledger_file.close()
            return records
        ledger_file.seek(0)
        records = json.load(ledger_file)
        ledger_file.close()
        print("All the records data is:\n" + str(records))
        return records

    # Its a list that contains dicts that each is an account in the bank

    def __init__(self):
        self.connected_atms = []
        self.bank_records = Bank.get_records()

    @staticmethod
    def valid_id(id):
        """The function receives an id and makes sure that the id is valid. If not the user must enter a new id.
        The function returns the valid id the user entered"""
        while (not id.isdigit()) and (len(id) != 9):
            id = input("The id must contain 9 digits and it can only contain digits.\nPlease enter your id: ")
        return id

    @staticmethod
    def valid_name(name):
        """The function receives a name and makes sure that the name is valid. If not the user must enter a new name.
        The function returns the valid name the user entered"""
        temp_name = name.lower().replace(' ', '')
        while not temp_name.isalpha():
            name = input("The name must contain only letters, except if you are Elon Musk's son.\nPlease enter a name: ")
            temp_name = name.lower().replace(' ', '')
        return name

    @staticmethod
    def valid_code(code):
        """The function receives a code and makes sure that the code is valid. If not the user must enter a new code.
        The function returns the valid code the user entered"""
        while (not code.isdigit()) or len(code) != 4:
            code = input("The code must contain 4 digits.\nPlease enter a code: ")
        return code

    @staticmethod
    def valid_amount_of_money(money):
        """The function receives an amount of money and makes sure that the amount of money is valid. If not the user
        must enter a new amount of money. The function returns a valid amount of money"""
        temp = money.replace('.', '', 1)
        while len(temp) == 0 or not ((temp[0] == "-" and temp[1:].isdigit()) or (temp[0] != "-" and temp.isdigit())):
            money = input("The balance must be a number.\nPlease enter a code: ")
            temp = money.replace('.', '', 1)
        return money

    def create_an_account(self, id, name, code, balance):
        """The function creates a new account in the bank"""
        account = {"Id": id,
                   "Name": name,
                   "Code": code,
                   "Balance": balance}
        self.bank_records.append(account)
        print("The new list is: " + str(self.bank_records))

    def save_records(self):
        """The function saves the list of accounts that we used in the bank in a text file"""
        all_data_to_save = self.bank_records
        ledger_file = open(Bank.ledger_file_path, "w")
        json.dump(all_data_to_save, ledger_file)
        ledger_file.close()

    def validate_secret_code(self, id, code):
        """The function receives a person's id and a secret code and returns True if there is an account with
        that id and secret code and False otherwise"""
        for account in self.bank_records:
            if account["Id"] == id and account["Code"] == code:
                return True
        return False

    def is_name_in_records(self, name):
        """The function checks if a name exists in the bank's records"""
        for account in self.bank_records:
            if account["Name"] == name:
                return True
        return False

    def is_id_in_records(self, id):
        """The function checks if a id exists in the bank's records"""
        for account in self.bank_records:
            if account["Id"] == id:
                return True
        return False

    def make_sure_account_has_money(self, id, amount_of_money):
        """The function returns True if the account with the given name has the given amount of money in it's account"""
        for account in self.bank_records:
            if account["Id"] == id and account["Balance"] >= amount_of_money:
                return True
        return False

    def check_account_balance(self, id):
        """The function returns the balance of the account with the given id.
        If the account doesn't exists return the minimum value of float"""
        for account in self.bank_records:
            if account["Id"] == id:
                return account["Balance"]
        return sys.float_info.min

    def make_a_transition(self, from_id, from_code, to_id, amount_of_money):
        """If possible the function makes a transition of the given amount of money from a given account to another
        given account"""
        if not self.is_id_in_records(from_id):
            print("Sorry but who is this person you are trying to send money from?")
        elif not self.is_id_in_records(to_id):
            print("Sorry but who is this person you are trying to send money to?")
        elif not self.validate_secret_code(from_id, from_code):
            print("The secret code is invalid! Police arrest this guy.")
        elif from_id == to_id:
            print("Are you trying to send money to yourself? It doesn't work that way but nice try")
        elif not self.make_sure_account_has_money(from_id, amount_of_money):
            print("Sorry mate, but you don't have enough money to send")
        else:
            for account in self.bank_records:
                if account["Id"] == from_id:
                    account["Balance"] -= amount_of_money
                elif account["Id"] == to_id:
                    account["Balance"] += amount_of_money


def handle_bank():
    bank = Bank()
    bank_activated = True
    print("The bank is ready!")
    while bank_activated:
        print("\nEnter 1 to create an account.\nEnter 2 to validate secret code.\nEnter 3 to make a transition."
              "\nEnter 4 to check your balance.\nEnter 5 to save the latest records.\nEnter 6 to exit the system.\n")
        user_input = input("Input: ")
        if user_input == "1":
            id = input("Please enter your id: ")
            id = Bank.valid_id(id)
            name = input("Please enter a name: ")
            name = Bank.valid_name(name)
            code = input("Please enter a code: ")
            code = Bank.valid_code(code)
            balance = input("Please enter how much money you have in your balance: ")
            balance = float(Bank.valid_amount_of_money(balance))  # Make sure that the string is valid then convert to float
            bank.create_an_account(id, name, code, balance)
        elif user_input == "2":
            name = input("\nPlease enter the name of the account: ")
            name = Bank.valid_name(name)
            secret_code = input("Please enter the secret code of the account: ")
            secret_code = Bank.valid_code(secret_code)
            if bank.validate_secret_code(name, secret_code):
                print("\nYes the secret code and name match!")
            else:
                print("\nWait... you sure you have the right information? Maybe you should try again")
        elif user_input == "3":
            from_id = input("\nPlease enter the id of the person you are trying to send money from: ")
            from_id = Bank.valid_id(from_id)
            secret_code = input("Please enter the secret code of the person that tries to send money from: ")
            secret_code = Bank.valid_code(secret_code)
            to_id = input("Please enter the id of the person you are trying to send money to: ")
            to_id = Bank.valid_id(to_id)
            money = input("How much money to transfer: ")
            money = float(Bank.valid_amount_of_money(money))  # Make sure that the string is valid then convert to float
            bank.make_a_transition(from_id, secret_code, to_id, money)
        elif user_input == "4":
            id = input("\nPlease enter an id: ")
            id = Bank.valid_id(id)
            balance = bank.check_account_balance(id)
            if balance != sys.float_info.min:
                print("\nThe account has: " + str(balance) + " dollars in the account.")
            else:
                print("\nThe account id is invalid.")
        elif user_input == "5":
            bank.save_records()
            print("\nCheck!")
        elif user_input == "6":
            bank_activated = False
        else:
            print("Huh?")


def main():
    handle_bank()


if __name__ == "__main__":
    main()
