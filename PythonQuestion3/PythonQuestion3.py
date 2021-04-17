
def receive_String():
    """The function returns a string the user enters"""
    return input("Please enter a string\n")


def compress_string(input_string):
    """The function receives a string and returns the string but compressed"""
    compressed_string = ""
    if input_string != "":
        compressed_string = input_string[0]  # We save the first char before checking the other chars
        index = 1  # Start checking from the second char
        count = 1
        while index < len(input_string):
            if input_string[index] != input_string[index-1]:
                # If the current char is not equal to the previous char - print the number of encounters with the
                # previous char and start counting the encounters with the new current char
                compressed_string += str(count)
                compressed_string += input_string[index]
                count = 1
            else:
                count += 1  # If the previous char is the same as the current char increase the number of encounters
            index += 1
        compressed_string += str(count)
    return compressed_string


def handle_string():
    """The fucntion receives a string and compresses it and prints the result"""
    input_string = receive_String()
    print("Before compression: " + input_string + "\n")
    compressed_string = compress_string(input_string)
    print("After compression: " + compressed_string + "\n")


def main():
    handle_string()

if __name__ == "__main__":
    main()