
def sum_numbers_from_multiple_inputs():
    """The function receives numbers from multiple inputs and returns the sum of the given numbers"""
    # The given numbers are integers
    sum_numbers = 0
    user_input = input("Please enter a number. To stop please enter the work stop\n")
    while user_input != "stop":
        sum_numbers += int(user_input) # The input must be a number if it's not the word stop
        user_input = input("Please enter a number. To stop please enter the work stop\n")
    print("The sum of the numbers is: " + str(sum_numbers) + "\n")


def main():
    sum_numbers_from_multiple_inputs()

if __name__ == "__main__":
    main()