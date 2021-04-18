
def multi(element):
    """The function receives a number and returns the number multiplied by 2."""
    return element * 2


def map(function, list):
    """The function receives a function and a list.
    The function returns a new list in which each element is equal to an element in the given list after activating 
    the given function on the element.
    """
    new_list = []
    for element in list:
        new_list.append(function(element))
    return new_list


def print_list(list):
    """The function receives a list and prints the given list."""
    list_elements = ""
    for element in list:
        list_elements += str(element) + ", "
    print(list_elements)


def manage_assignemnt():
    """The function uses examplles to demonstrate the map function."""
    # Example 1
    func = multi
    list = [1,2,3]
    print("List before: ")
    print_list(list)

    new_list = map(func, list)
    print("List after: ")
    print_list(new_list)

    # Example 2
    func = sum  # Sum is a built in function
    list = [(2, 4), (1, 4, 2), (1, 3, 5, 6, 2), (3, )]
    print("List before: ")
    print_list(list)

    new_list = map(func, list)
    print("List after: ")
    print_list(new_list)


def main():
    manage_assignemnt()


if __name__ == "__main__":
    main()
