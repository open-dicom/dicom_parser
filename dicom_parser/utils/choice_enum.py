from enum import Enum
from typing import Tuple


class ChoiceEnum(Enum):
    """
    An :class:`~enum.Enum` with a custom `class method`_ that facilitates
    integration with a Django_ :class:`~django.db.models.Field`'s
    :attr:`~django.db.models.Field.choices` attribute.


    .. _class method:
       https://realpython.com/instance-class-and-static-methods-demystified/#class-methods
    .. _Django: https://www.djangoproject.com/
    """

    @classmethod
    def choices(cls) -> Tuple[Tuple[str, str], ...]:
        """
        Returns the contained items as a tuple of tuples.

        Returns
        -------
        Tuple[Tuple[str, str], ...]
            Tuple of (name, value) tuples
        """

        return tuple([(item.name, item.value) for item in cls])
