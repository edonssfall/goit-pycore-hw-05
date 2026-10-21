import os


def check_path(path: str) -> None:
    """
    check that path exists and the app has permission to read it
    :param path: path to check
    :return: None, raises an exception if the check fails
    """
    if not path:
        raise Exception(f'path must be set')

    if not os.path.exists(path):
        raise Exception(f'{path} is not exists or dont have enough permissions')

    if not os.access(path, os.R_OK):
        raise PermissionError(f'No permission to read {path}')


def parse_value(value, type, name):
    """
    convert value to a type, raise a readable error if it fails
    :param value: value to test
    :param type: class to convert value with (e.g. int)
    :param name: field name for the error message
    :return: converted value or raise
    """
    try:
        return type(value)
    except Exception:
        raise Exception(f'{name}: {value} have not valid format')
