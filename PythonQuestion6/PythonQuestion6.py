
import time

cache = {}  # It's a global variable that saves the results of the heavy function
keys = []  # A list that saves the keys in the cache

CACHE_MAX_CAPACITY = 100  # It's the capacity of the cache. It is needed so the cache won't grow without a limit


def heavy_function(*args):
    """The function just sums the values of its arguments and returns the result.
    I added a delay so we can see that the cache helps improve the function's running time.
    """
    time.sleep(3)  # The delay
    result = sum(args)  # Just a simple sum function
    return result


def heavy_function_with_cache(*args):
    """The function is a decorator which means it wraps the heavy function we are using.
    If the given arguments were used in the past, the function can get their result from it's cache.
    If the given arguments weren't used in the past, the decorator calls the heavy function with the given arguments
    and returns the result of the function after saving it in the cache.
    """
    # First of all we'll check if the arguments were used in the past
    if args in cache:
        return cache[args]

    # Now add a new pair to the cache
    print("The length of the dictionary is: " + str(len(cache)))
    if len(cache) == CACHE_MAX_CAPACITY:
        # Need to clear up dome space in the cache
        oldest_key = keys.pop(0)
        del cache[oldest_key]
    cache[args] = heavy_function(*args)  # Save the result in the cache
    keys.append(args)
    return cache[args]


def handle_assignment():
    """This function shows examples to demonstrate how the cache works."""
    # Examples
    start_time = time.perf_counter()
    print("The function receives: 1,2,3")
    print("The function outputs: " + str(heavy_function_with_cache(1,2,3)))
    end_time = time.perf_counter()
    print("The function took: " + str(end_time-start_time) + " seconds.\n")

    start_time = time.perf_counter()
    print("The function receives: 7,-3,4,1")
    print("The function outputs: " + str(heavy_function_with_cache(7,-3,4,1)))
    end_time = time.perf_counter()
    print("The function took: " + str(end_time-start_time) + " seconds.\n")

    start_time = time.perf_counter()
    print("The function receives: 1,2,3")
    print("The function outputs: " + str(heavy_function_with_cache(1,2,3)))
    end_time = time.perf_counter()
    print("The function took: " + str(end_time-start_time) + " seconds.\n")

    start_time = time.perf_counter()
    print("The function receives: 1,2")
    print("The function outputs: " + str(heavy_function_with_cache(1,2)))
    end_time = time.perf_counter()
    print("The function took: " + str(end_time-start_time) + " seconds.\n")

    start_time = time.perf_counter()
    print("The function receives: 1,2")
    print("The function outputs: " + str(heavy_function_with_cache(1,2)))
    end_time = time.perf_counter()
    print("The function took: " + str(end_time-start_time) + " seconds.\n")


def main():
    handle_assignment()


if __name__ == "__main__":
    main()
