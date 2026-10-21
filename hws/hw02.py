import re
from typing import Callable


def generator_numbers(text: str):
    """
    lazily find numbers in text with a regex (separated by spaces, two decimal places)
    :param text: text to search
    :return: generator that yields each number as float
    """
    for val in text.split():
        try:
            if re.match(r'(?<!\S)\d+\.\d{2}(?!\S)', val):
                yield float(val)
        except ValueError:
            continue


def sum_profit(text: str, func: Callable):
    """
    sum all numbers that func finds in text
    :param text: text to search
    :param func: function that takes text and yields numbers (e.g. generator_numbers)
    :return: sum of all numbers found in text
    """
    total = 0.0
    f = func(text)
    while True:
        try:
            total += next(f)
        except StopIteration:
            break
    return total
