"""
Definition of the :class:`~dicom_parser.utils.choice_enum.ChoiceEnum` class,
which is used to facilitate the usage of :class:`~enum.Enum` definitions with Django_
Field_ choices_.

.. _choices: https://docs.djangoproject.com/en/3.0/ref/models/fields/#choices
.. _Django: https://www.djangoproject.com/
.. _Field: https://docs.djangoproject.com/en/3.0/ref/models/fields/#django.db.models.Field

"""

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
