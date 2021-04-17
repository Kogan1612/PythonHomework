
def receive_id():
    """The function receives an id from the user
    If the id isn't an integer the function will return -1
    """
    id = input("Please enter an id\n")
    if id.isnumeric():
        return int(id)
    else:
        print("There is a problem with the id")
        return -1


def is_check_digit_valid(id):
    """The function receives an id which is an integer between 100000000 and 999999999
    The function returns True if the check digit of the id is valid and False otherwise
    """
    coefficients = [1,2,1,2,1,2,1,2]
    sum = 0
    index = len(coefficients) - 1
    check_digit = id % 10  # The check digit is the first digit, the most insignificant digit in the id
    id = int(id / 10)
    # We are checking the id's digits from right to left
    while id > 0:
        digit = id % 10
        addition = coefficients[index] * digit
        if addition >= 10:
            addition = (addition % 10) + int(addition / 10)
        sum += addition
        id = int(id / 10)
        index -= 1
    # The first digit of the sum is the only digit that matters because we are looking for a complementary number to 10
    sum_first_digit = sum % 10  
    if sum_first_digit > 5:
        complementary_number = 10 - sum_first_digit
    else:
        complementary_number = sum_first_digit

    if check_digit == complementary_number:
        return True
    return False


def is_id_valid(id):
    """The function receives an id and returns a message whether the id is valid or not"""
    if 100000000 > id or id > 999999999:
        print("The length of the id is invalid")
    elif is_check_digit_valid(id):
        print("The check digit of the id is valid")
    else:
        print("The check digit of the id is invalid")


def manage_id():
    """The function receives an id from the user and prints a message if the given id is valid"""
    id = receive_id()
    if id != -1:
        is_id_valid(id)

def main():
    manage_id()

if __name__ == "__main__":
    main()