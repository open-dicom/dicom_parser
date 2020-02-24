"""
Definition of parser that accepts
:class:`~dicom_parser.utils.siemens.data_element.CsaDataElement`
instances to be parsed and keeps a pointer to a dictionary that
may aggregate the results.

"""

from dicom_parser.utils.siemens.csa.data_element import CsaDataElement


class CsaParser:
    """
    Parses CSA header data elements given as
    :class:`~dicom_parser.utils.siemens.data_element.CsaDataElement`
    instances into a public dictionary.

    """

    def __init__(self, destination: dict = None):
        """
        The parser may be initialized with an existing dictionary instance.

        Parameters
        ----------
        destination : dict, optional
            Dictionary instance to update with the parsed values, by default None
        """

        self.parsed = destination if isinstance(destination, dict) else {}

    def update_existing_element_list(
        self, part_name: str, index: int, destination: dict
    ) -> dict:
        """
        If an array part (part containing the `[<index>]` pattern) exists as any part
        of the listed key except for the last, it indicates a list of dictionary
        instances. This method check whether a dictionary exists already at the given
        list's index. If it does, returns that dict instance, otherwise, creates a new one
        and returns it.

        Parameters
        ----------
        part_name : str
            The list's key within the destination dictionary
        index : int
            The index of the nested part
        destination : dict
            The current level of scaffolding within the parsed dictionary

        Returns
        -------
        dict
            The next level of the key's scaffolding within the parsed dictionary
        """

        try:
            return destination[part_name][index]
        except IndexError:
            destination[part_name].append({})
            return destination[part_name][-1]

    def create_new_element_list(self, part_name: str, destination: dict) -> dict:
        """
        If an array part (part containing the `[<index>]` pattern) exists as any part
        of the listed key except for the last, it indicates a list of dictionary
        instances. This method creates a new list with a single dict instances and
        returns a pointer to it.

        Parameters
        ----------
        part_name : str
            The key for the list in the current dict level of the constructed
            scaffolding.
        destination : dict
            The current level of scaffolding within the parsed dictionary

        Returns
        -------
        dict
            The next level of the key's scaffolding within the parsed dictionary
        """

        destination[part_name] = [{}]
        return destination[part_name][0]

    def scaffold_list_part(self, part: str, index: int, destination: dict) -> dict:
        """
        Returns the destination of a given key's list part within the parsed dictionary.

        Parameters
        ----------
        part : str
            List part's name
        index : int
            The index within the list for the next part in the nested key
        destination : dict
            The current level of scaffolding within the parsed dictionary

        Returns
        -------
        dict
            The next level of the key's scaffolding within the parsed dictionary
        """

        part_name = part.split("[")[0]
        existing_list = isinstance(destination.get(part_name), list)
        if existing_list:
            return self.update_existing_element_list(part_name, index, destination)
        else:
            return self.create_new_element_list(part_name, destination)

    def scaffold_dict_part(self, part: str, destination: dict) -> dict:
        """
        Returns the destination of a given key's dict part within the parsed dictionary.

        Parameters
        ----------
        part : str
            List part's name
        destination : dict
            The current level of scaffolding within the parsed dictionary

        Returns
        -------
        dict
            The next level of the key's scaffolding within the parsed dictionary
        """

        if isinstance(destination.get(part), dict):
            return destination[part]
        else:
            destination[part] = {}
            return destination[part]

    def scaffold_part(
        self, csa_data_element: CsaDataElement, part: str, destination: dict
    ) -> dict:
        """
        Returns the destination of a given key's part within the parsed dictionary.

        Parameters
        ----------
        csa_data_element : :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            The source instance
        part : str
            List part's name
        destination : dict
            The current level of scaffolding within the parsed dictionary

        Returns
        -------
        dict
            The next level of the key's scaffolding within the parsed dictionary
        """

        list_index = csa_data_element.search_array_pattern(part)
        if list_index is not None:
            return self.scaffold_list_part(part, list_index, destination)
        else:
            return self.scaffold_dict_part(part, destination)

    def scaffold_listed_key(
        self, csa_data_element: CsaDataElement, destination: dict = None
    ) -> dict:
        """
        Creates a scaffolding within the parsed values dictionary. This means that it
        runs over the data elements nested key structure
        (LevelA.ListLevelB[5].LevelC = 'value') and returns a pointer to the appropriate
        destination for the value within the parsed values dictionary.

        Parameters
        ----------
        csa_data_element : :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            Instance to scaffold a destination for
        destination : dict, optional
            An existing destination dictionary, by default None

        Returns
        -------
        dict
            A pointer to the appropriate destination for the
            :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`'s value
        """

        destination = destination if isinstance(destination, dict) else {}
        for part in csa_data_element.key[:-1]:
            destination = self.scaffold_part(csa_data_element, part, destination)
        return destination

    def assign_list_element(self, part: str, value, destination: dict):
        """
        Appends to an existing list value or creates a new list instance for it.

        Parameters
        ----------
        part : str
            Last part's name
        value : [type]
            The :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`'s
            value
        destination : dict
            A pointer to the appropriate destination with the parsed dictionary
        """

        part_name = part.split("[")[0]
        try:
            destination[part_name].append(value)
        except (KeyError, AttributeError):
            destination[part_name] = [value]

    def assign_listed_element(
        self, csa_data_element: CsaDataElement, destination: dict
    ):
        """
        Once the destination for the
        :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`'s
        value has been retrieved or created, this method assigns the value at
        that destination.

        Parameters
        ----------
        csa_data_element : :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            The instance from which to assign the value
        destination : dict
            The appropriate destination within the parsed values dictionary
        """

        last_part = csa_data_element.key[-1]
        value = self.fix_value(csa_data_element.value)
        list_match = csa_data_element.search_array_pattern(last_part)
        if list_match:
            self.assign_list_element(last_part, value, destination)
        else:
            destination[last_part] = value

    def fix_value(self, value):
        """
        Covert a CSA header element's value to float or int if possible.
        Also cleans up redundant quotation marks and decodes hexadecimal values.

        Parameters
        ----------
        value : [type]
            Some CSA header element value

        Returns
        -------
        str, int, or float
            Fixed (converted) value
        """

        try:
            return (
                int(value.split(".")[0]) if float(value).is_integer() else float(value)
            )
        except ValueError:
            # Decode hexadecimal string
            try:
                return int(value, 16)
            except ValueError:
                # Remove extra quotes from strings
                # e.g. '""Siemens""' -> 'Siemens'
                return value.strip('"')

    def parse(self, csa_data_element: CsaDataElement):
        """
        Parses a raw CSA header element into the provided dictionary or creates
        a new one.

        Parameters
        ----------
        csa_data_element : :class:`~dicom_parser.utils.siemens.csa.data_element.CsaDataElement`
            CSA header element to be parsed
        """

        destination = self.scaffold_listed_key(csa_data_element, self.parsed)
        self.assign_listed_element(csa_data_element, destination)
        return self.parsed
