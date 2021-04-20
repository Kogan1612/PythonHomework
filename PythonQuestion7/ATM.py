import socket
import threading


class ATM:
    HOST = "127.0.0.1"
    PORT = 65432

    @staticmethod
    def connect_to_bank():
        """The function connects the ATM object to the bank"""
        atm_socket = socket.socket()  # Create a socket object
        try:
            atm_socket.connect((ATM.HOST, ATM.PORT))  # Connect the ATM with the Bank
        except:
            print("The bank isn't working right now please try again later.")
            exit(0)  # Exit the program
        return atm_socket

    @staticmethod
    def valid_id(id):
        """The function receives an id and makes sure that the id is valid. If not the user must enter a new id.
        The function returns the valid id the user entered"""
        while (not id.isdigit()) or (len(id) != 9):
            id = input("The id must contain 9 digits and it can only contain digits.\nPlease enter your id: ")
        return id

    @staticmethod
    def valid_name(name):
        """The function receives a name and makes sure that the name is valid. If not the user must enter a new name.
        The function returns the valid name the user entered"""
        # A name can have a space in it so replace it to check if all else is letters
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
        # An amount of money can contain a '.' so replace it to see if all else is numbers
        temp = money.replace('.', '', 1)
        while len(temp) == 0 or not temp.isdigit():  # Amount of money cannot be negative
            money = input("The amount of money must be a positive number.\nPlease enter an amount: ")
            temp = money.replace('.', '', 1)
        return money

    @staticmethod
    def validate_balance(balance):
        """The function receives a balance and makes sure that the balance is valid. If not the user
        must enter a new balance. The function returns a valid balance."""
        # An amount of money can contain a '.' so replace it to see if all else is numbers
        temp = balance.replace('.', '', 1)
        while len(temp) == 0 or not ((temp[0] == "-" and temp[1:].isdigit()) or (temp[0] != "-" and temp.isdigit())):
            balance = input("The balance must be a number.\nPlease enter a balance: ")
            temp = balance.replace('.', '', 1)
        return balance

    def receive_messages_from_bank(self):
        """The function tries to receives a message from the bank until the user stops using the ATM"""
        while self.user_using_atm:
            try:
                data = self.socket.recv(1024).decode()
                if len(data) != 0:
                    print("\nThe bank said: " + data)  # Print message from the bank
                    self.latest_message = data
            except:
                pass

    def wait_for_message(self):
        """The function waits for a message to arrive from the bank.
        The code will stop until a message will arrive."""
        while len(self.latest_message) == 0:
            pass
        self.latest_message = ""  # Delete the message in the attribute so we can check it again ion the future

    def atm_user_interface(self):
        """The function handles the user's requests.
        It is the main function that manages the ATM and talks to the bank."""
        print("The User is ready!")
        listener_thread = threading.Thread(target=self.receive_messages_from_bank)
        listener_thread.start()  # Start the thread that listens for messages from the bank
        while self.user_using_atm:
            print("\nATM Options:\nEnter 1 to create an account.\nEnter 2 to validate secret code.\nEnter 3 to make a "
                  "transaction.\nEnter 4 to check your balance.\nEnter 5 to exit the system.\n")
            user_input = input("Input: ")
            if user_input == "1":
                id = input("Please enter your id: ")
                id = ATM.valid_id(id)  # Validate id
                name = input("Please enter a name: ")
                name = ATM.valid_name(name)  # Validate name
                code = input("Please enter a code: ")
                code = ATM.valid_code(code)  # Validate secret code
                balance = input("Please enter how much money you have in your balance: ")
                balance = ATM.validate_balance(balance)  # Validate balance
                message = "1*" + id + "*" + name + "*" + code + "*" + balance
                self.socket.send(message.encode())
                self.wait_for_message()
            elif user_input == "2":
                id = input("\nPlease enter the id of the account: ")
                id = ATM.valid_id(id)  # Validate id
                secret_code = input("Please enter the secret code of the account: ")
                secret_code = ATM.valid_code(secret_code)  # Validate secret code
                message = "2*" + id + "*" + secret_code
                self.socket.send(message.encode())
                self.wait_for_message()
            elif user_input == "3":
                from_id = input("\nPlease enter the id of the person you are trying to send money from: ")
                from_id = ATM.valid_id(from_id)  # Validate id
                secret_code = input("Please enter the secret code of the person that tries to send money from: ")
                secret_code = ATM.valid_code(secret_code)  # Validate secret code
                to_id = input("Please enter the id of the person you are trying to send money to: ")
                to_id = ATM.valid_id(to_id)  # Validate id
                money = input("How much money to transfer: ")
                money = ATM.valid_amount_of_money(money)  # Validate amount of money
                message = "3*" + from_id + "*" + secret_code + "*" + to_id + "*" + money
                self.socket.send(message.encode())
                self.wait_for_message()
            elif user_input == "4":
                id = input("\nPlease enter an id: ")
                id = ATM.valid_id(id)  # Validate id
                message = "4*" + id
                self.socket.send(message.encode())
                self.wait_for_message()
            elif user_input == "5":
                message = "5"
                self.socket.send(message.encode())
                self.user_using_atm = False
            else:
                print("Huh?")
        print("\nBye!")
        self.socket.close()  # The user finished using the ATM

    def __init__(self):
        self.socket = ATM.connect_to_bank()
        self.user_using_atm = True
        self.latest_message = ""


def main():
    atm = ATM()
    atm.atm_user_interface()


if __name__ == "__main__":
    main()
