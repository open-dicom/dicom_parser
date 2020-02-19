"""
Based on `this <https://stackoverflow.com/a/664239/4416932>`_
StackOverflow answer.

"""

import itertools

from types import GeneratorType


def peek(iterable: GeneratorType) -> tuple:
    """
    From `Wikipedia <https://en.wikipedia.org/wiki/Peek_%28data_type_operation%29>`_:
    "peek is an operation which returns the value of the top of the collection without removing the value from the data."

    
    Parameters
    ----------
    iterable : GeneratorType
        A generator object to peek into.
    
    Returns
    -------
    tuple
        A tuple containing the first item and the original generator, unless it is empty, then (None, None).
    """

    try:
        first = next(iterable)
    except StopIteration:
        return None, None
    return first, itertools.chain([first], iterable)
