import socket
import threading
import time
import json
import sys
import os.path


class Bank:

    ledger_file_path = "Ledger.txt"
    HOST = "127.0.0.1"
    PORT = 65432

    def connect_to_atms(self):
        """The function tries to connect to ATMs - it is used as a thread"""
        bank_socket = socket.socket()  # Create a socket
        bank_socket.bind((Bank.HOST, Bank.PORT))  # Bind socket to port and ip address
        bank_socket.listen(5)  # The TCP listener starts
        while True:
            connection, address = bank_socket.accept()  # waiting until someone connects
            print("Another ATM connected!")
            self.connected_atms[self.thread_count] = connection
            self.thread_count += 1
            print("We now have " + str(len(self.connected_atms)) + " connected ATMs")
            main_thread = threading.Thread(target=self.handle_atm, args=(self.thread_count-1, ))  # The args is a tuple
            main_thread.start()  # Start the thread that handles the atm's requests
        bank_socket.close()

    def services_lock(self):
        """The function locks the balance services.
        If the services are already locked the function will wait until they are unlocked and then it will lock them."""
        # Lock if someone is already using the bank's balance services
        if self.records_lock:
            print("Lock is activated. Need to wait.")
            self.wait_for_lock_to_end()
        print("Locked")
        self.records_lock = True

    def wait_for_lock_to_end(self):
        """The function waits until the services are unlocked."""
        while self.records_lock:
            pass

    def services_unlock(self):
        """The function unlocks the balance services."""
        print("Unlocked")
        self.records_lock = False

    def handle_atm(self, connection_id):
        """After a connecting to an ATM, the function is in charge of giving service to the ATM and
        handle requests from the ATM - the function is used as a thread"""
        connection = self.connected_atms[connection_id]
        atm_working = True
        while atm_working:
            try:
                data = connection.recv(1024).decode()
            except:
                continue
            if len(data) == 0:
                continue
            data_parts = data.split("*")  # The sent data has * to divide it's parts
            if data_parts[0] == "1":
                print("\nProtocol 1")
                id = data_parts[1]
                name = data_parts[2]
                code = data_parts[3]
                balance = float(data_parts[4])
                self.services_lock()  # Lock balance services
                if self.create_an_account(id, name, code, balance):  # Create an account
                    message = "Account Created.\n"
                else:
                    message = "Id is taken. You are an impostor\n"
                self.services_unlock()  # Unlock balance services
                connection.send(message.encode())
                print("Sent to ATM from protocol 1")
            elif data_parts[0] == "2":
                print("\nProtocol 2")
                id = data_parts[1]
                code = data_parts[2]
                if self.validate_secret_code(id, code):
                    message = "Yes, the code matches the id\n"
                else:
                    message = "No, the code doesn't match the id\n"
                connection.send(message.encode())
                print("Sent to ATM from protocol 2")
            elif data_parts[0] == "3":
                print("\nProtocol 3")
                from_id = data_parts[1]
                code = data_parts[2]
                to_id = data_parts[3]
                money = float(data_parts[4])
                self.services_lock()  # Lock balance services
                message = self.make_a_transaction(from_id, code, to_id, money)
                self.services_unlock()  # Unlock balance services
                connection.send(message.encode())
                print("Sent to ATM from protocol 3")
            elif data_parts[0] == "4":
                print("\nProtocol 4")
                id = data_parts[1]
                self.services_lock()  # Lock balance services
                balance = self.check_account_balance(id)
                self.services_unlock()  # Unlock balance services
                if balance != sys.float_info.min:
                    message = "The account has: " + str(balance) + "$"
                else:
                    message = "Invalid id"
                connection.send(message.encode())
                print("Sent to ATM from protocol 4")
            elif data_parts[0] == "5":
                print("\nProtocol 5")
                atm_working = False
        del self.connected_atms[connection_id]
        print("Bye ATM!")
        print("We now have " + str(len(self.connected_atms)) + " connected ATMs")
        connection.close()

    @staticmethod
    def get_records():
        """The function gets the record fro, the ledger file and if the file doesn't exists it creates a new file"""
        records = []
        # First check that the file exists - if it doesn't lets create a new one
        if not os.path.isfile(Bank.ledger_file_path):
            # Create a new file for the bank's ledger
            temp_file = open(Bank.ledger_file_path, "w+")  # Used to create a file for the bank's ledger
            temp_file.close()  # Close the file that we just created
        # Now the ledger exists for sure so we need to read from it
        ledger_file = open(Bank.ledger_file_path, "r")
        # If the ledger is empty we don't have any records yet so we return an empty record list
        if len(ledger_file.readlines()) == 0:
            print("Empty records")
            ledger_file.close()
            return records
        ledger_file.seek(0)
        records = json.load(ledger_file)
        ledger_file.close()
        print("All the records data is:\n" + str(records))
        return records

    def __init__(self):
        self.connected_atms = {}
        self.bank_records = Bank.get_records()  # A list that contains dictionaries that each is an account in the bank
        self.thread_count = 0  # Count how many threads ran so far - it gives a unique id to a thread
        self.records_lock = False
        connection_thread = threading.Thread(target=self.connect_to_atms)
        connection_thread.start()  # Start the thread that waits for the atms to connect

    def save_records(self):
        """The function saves the list of accounts that we used in the bank in a text file"""
        all_data_to_save = self.bank_records
        ledger_file = open(Bank.ledger_file_path, "w")
        json.dump(all_data_to_save, ledger_file)
        ledger_file.close()

    def create_an_account(self, id, name, code, balance):
        """The function creates a new account in the bank"""
        if self.is_id_in_records(id):
            print("ID EXISTS")
            return False
        account = {"Id": id,
                   "Name": name,
                   "Code": code,
                   "Balance": balance}
        self.bank_records.append(account)
        print("The new list is: " + str(self.bank_records))
        self.save_records()
        return True

    def validate_secret_code(self, id, code):
        """The function receives a person's id and a secret code and returns True if there is an account with
        that id and secret code and False otherwise"""
        for account in self.bank_records:
            if account["Id"] == id and account["Code"] == code:
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

    def make_a_transaction(self, from_id, from_code, to_id, amount_of_money):
        """If possible the function makes a transition of the given amount of money from a given account to another
        given account"""
        time.sleep(10)  # I'm adding a delay to check if two transactions can occur simultaneously
        if not self.is_id_in_records(from_id):
            return "Sorry but who is this person you are trying to send money from?"
        elif not self.is_id_in_records(to_id):
            return "Sorry but who is this person you are trying to send money to?"
        elif not self.validate_secret_code(from_id, from_code):
            return "The secret code is invalid! Police arrest this guy."
        elif from_id == to_id:
            return "Are you trying to send money to yourself? It doesn't work that way but nice try."
        elif not self.make_sure_account_has_money(from_id, amount_of_money):
            return "Sorry mate, but you don't have enough money to send."
        else:
            for account in self.bank_records:
                if account["Id"] == from_id:
                    account["Balance"] -= amount_of_money
                elif account["Id"] == to_id:
                    account["Balance"] += amount_of_money
            self.save_records()
            return "the transaction is done"


def main():
    bank = Bank()


if __name__ == "__main__":
    main()

