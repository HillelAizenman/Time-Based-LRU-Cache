import os
import platform

from TimeBasedLruCache import TimeBasedLruCache


def start_menu_interface():
    print_welcome_message()
    capacity = positive_integer_input()
    cache = TimeBasedLruCache(capacity)

    get_value = None
    get_key = None
    while True:
        clear_screen()
        cache.print_cache()
        print_menu()
        get_was_called(get_key, get_value)
        get_value = None
        get_key = None
        user_input = option_integer_input()

        if user_input == 0:
            break

        if user_input == 1:
            key = key_string_input()
            value = value_integer_input()
            cache.put(key, value)

        elif user_input == 2:
            if cache.is_empty():
                get_key = "cache is empty"
                continue

            key = key_string_input()
            value = cache.get(key)
            if value:
                get_value = value
                get_key = key
            else:
                get_key = "key does not exist"

        elif user_input == 3:
            print("Enter number of seconds passed: ")
            seconds = positive_integer_input()
            cache.clear_expired(seconds)


def positive_integer_input():
    while True:
        try:
            number = int(input())
            if number < 0:
                print("please enter a positive integer")
                continue
            return number
        except ValueError:
            print("please enter a positive integer")
            continue


def key_string_input():
    while True:
        print("Enter key: ", end="")
        key = input()
        if key != "" and not key[0].isspace():
            return key
        print("key shouldn't start with white space")


def value_integer_input():
    while True:
        try:
            print("Enter value: ", end="")
            number = int(input())
            return number
        except ValueError:
            print("please enter an integer")
            continue


def option_integer_input():
    while True:
        try:
            user_input = int(input())
            if 0 <= user_input <= 3:
                return user_input
            print("please enter a number between 0 and 3")
            continue
        except ValueError:
            print("please enter a number between 0 and 3")
            continue


def print_welcome_message():
    print("""Welcome to the LRU Cache Interface!
For the best experience, it's recommended to run this program in a terminal rather than within an IDE console.
The terminal provides a more aesthetic and functional interface.
Enter cache capacity: """)


def print_menu():
    print("""0. Exit
1. Put new element
2. Get element value
3. Clear expired
""")


def clear_screen():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def get_was_called(get_key, get_value):
    if get_key is not None:
        if get_value is not None:
            print(f"{get_key}: {get_value}")
        else:
            print(f"{get_key}")

