from enum import Enum


class ChoiceEnum(Enum):
    """
    A small adaptation to python's built-in :class:`~enum.Enum` class.
    
    """

    @classmethod
    def choices(cls) -> tuple:
        """
        Returns a tuple of tuples containing the name and the value of each
        item.
        
        Returns
        -------
        tuple
            (name, value) tuples representing each item.
        """
        return tuple([(item.name, item.value) for item in cls])
