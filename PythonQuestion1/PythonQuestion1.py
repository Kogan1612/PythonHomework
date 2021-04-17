
def sum_numbers_from_multiple_inputs():
    """The function receives numbers from multiple inputs and returns the sum of the given numbers"""
    # Assumption: The given numbers are integers
    sum_numbers = 0  # The sum has a default value of zero
    user_input = input("Please enter a number. To stop please enter the work stop.\n")
    while user_input != "stop":
        try:
            sum_numbers += int(user_input)  # Validates that the input is indeed a number in a string type and if so add it
        except:
            pass  # If the string is not a number don't add it and continue
        user_input = input("Please enter a number. To stop please enter the work stop.\n")
    print("The sum of the numbers is: " + str(sum_numbers) + ".\n")

def sum_numbers_from_one_input():
    """The function receives a list of numbers from the user and returns the sum of the given list"""
    # Assumption: The given numbers are integers
    numbers_sum = 0  # The sum has a default value of zero
    user_input = input("Please enter a list of numbers seperated by commas with no spaces.\n")
    numbers_list = user_input.split(",")  # Splits the given string to get the numbers
    for number in numbers_list:
        try:     
            numbers_sum += int(number)  # Validates that the input is indeed a number in a string type and if so add it
        except:  
            pass  # If the string is not a number don't add it and continue
    print("The sum of the numbers is: " + str(numbers_sum) + ".\n")


def main():
    sum_numbers_from_multiple_inputs()
    sum_numbers_from_one_input()

if __name__ == "__main__":
    main()