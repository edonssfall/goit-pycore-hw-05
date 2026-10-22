import re
import sys

from colorama import Fore, init

CACHE = dict()


def input_error(func):
    """
    decorator for command handlers: turn input errors (ValueError, KeyError, IndexError)
    into a message for the user, so the bot keeps running
    :param func: command handler
    :return: wrapped function that returns the handler result or an error message
    """

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return Fore.RED + "Give me correct name and correct phone please."
        except KeyError:
            return Fore.RED + "Give me existing name."
        except IndexError:
            return Fore.RED + "Give me <command> <name> <phone-optional> please."

    return inner


def validate_args(*args) -> tuple[str, str]:
    """
    validate name and phone: check there are 2 args and validate them with regex
    :param args: name: str, phone: str
    :return: (name: str, phone: str); raises IndexError for wrong number of args, ValueError for invalid values
    """
    if len(args) != 2:
        raise IndexError
    name, phone = args
    if not re.fullmatch(r'[a-zA-Z]+', name):
        raise ValueError
    if not re.fullmatch(r'^\+?\d{9,12}', phone):
        raise ValueError
    return name, phone


def get_key(name: str):
    """
    search for a key in cache, ignoring case
    :param name: contact name: str
    :return: existing key in cache or None
    """
    res = None
    l_name = name.lower()
    for key in CACHE.keys():
        if l_name == key.lower():
            res = key
            break
    return res


@input_error
def add_contact(*args) -> str | None:
    """
    add contact to cache or overwrite an existing one
    :param args: name: str, phone: str
    :return: answer to print (errors are handled by input_error)
    """
    name, phone = validate_args(*args)
    if key := get_key(name):
        CACHE[key] = phone
    else:
        CACHE[name] = phone
    return 'Contact added'


@input_error
def change_contact(*args) -> str | None:
    """
    change phone of an existing contact (name ignoring case)
    :param args: name: str, phone: str
    :return: answer to print; raises KeyError if the contact does not exist (handled by input_error)
    """
    name, phone = validate_args(*args)
    if key := get_key(name):
        CACHE[key] = phone
        return 'Contact updated'
    raise KeyError


@input_error
def show_phone(*args) -> str | None:
    """
    show phone by name (ignoring case)
    :param args: name: str
    :return: phone: str; raises IndexError, ValueError or KeyError (handled by input_error)
    """
    if len(args) != 1:
        raise IndexError
    name = args[0]
    if not re.fullmatch(r'[a-zA-Z]+', name):
        raise ValueError
    if key := get_key(name):
        return CACHE[key]
    raise KeyError


@input_error
def show_all() -> str:
    """
    show all contacts from cache, if there are any
    :return: answer to print
    """
    if CACHE:
        return ''.join(
            f"{Fore.BLUE if i % 2 == 0 else Fore.YELLOW}{name}: {phone}\n"
            for i, (name, phone) in enumerate(CACHE.items())
        )
    return 'Nothing to show, because DB is empty'


def parse_input(user_input: str) -> tuple[str, list]:
    """
    split user input into a command (lowercase) and its args
    :param user_input: user input
    :return: (command: str, *args); raises Exception for empty input (handled in main)
    """
    if not user_input.strip():
        raise Exception('Please enter a command.')
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    """
    chatbot entry point: request-response loop; also catches errors outside handlers (empty input, exit, EOF)
    """
    print("Welcome to the assistant bot!")
    while True:
        try:
            user_input = input("Enter a command: ")
            cmd, *args = parse_input(user_input)

            if cmd in ['close', 'exit']:
                raise EOFError
            match cmd:
                case 'hello':
                    print('How can I help you?')
                case 'add':
                    print(add_contact(*args))
                case 'change':
                    print(change_contact(*args))
                case 'phone':
                    print(show_phone(*args))
                case 'all':
                    print(show_all().rstrip())
                case _:
                    print(Fore.RED + 'Invalid command.')
        except EOFError:
            print('\nGood bye!')
            sys.exit()
        except Exception as e:
            print(Fore.RED + f'Error: {e}')


if __name__ == '__main__':
    init(autoreset=True)
    main()
