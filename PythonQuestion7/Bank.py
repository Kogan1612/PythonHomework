import json
import os.path


class Bank:
    ledger_file_path = "Ledger.txt"

    @staticmethod
    def get_records():
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

    # Its a dict of lists that contains dicts that each is an

    def create_an_account(self):
        name = input("Please enter a name: ")
        code = input("Please enter a code: ")
        balance = int(input("Please enter how much money you have in your balance: "))
        account = {"Name": name,
                   "Code": code,
                   "Balance": balance}
        self.bank_records.append(account)
        print("The new list is: " + str(self.bank_records))

    def save_records(self):
        all_data_to_save = self.bank_records
        ledger_file = open(Bank.ledger_file_path, "w")
        json.dump(all_data_to_save, ledger_file)
        ledger_file.close()

    def __init__(self):
        self.connected_atms = []
        self.bank_records = Bank.get_records()


def handle_bank():
    bank = Bank()
    user_input = ""
    while user_input != "2":
        user_input = input("Enter 1 to create an account.\nEnter 2 to exit and save.\nInput: ")
        if user_input == "1":
            bank.create_an_account()
        if user_input == "2":
            bank.save_records()


def main():
    handle_bank()


if __name__ == "__main__":
    main()
