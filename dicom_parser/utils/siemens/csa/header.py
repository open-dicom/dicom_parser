import re


class CsaHeader:
    ENCODING = "ISO-8859-1"
    HEADER_INFORMATION_PATTERN = r"### ASCCONV BEGIN(.*)### ASCCONV END ###"
    ELEMENT_PATTERN = r"([A-Z][^\n]*)"
    KEY_PATTERN = r"[A-Z].*"
    LIST_KEY_PATTERN = r"\[\d+\]"

    def __init__(self, header: bytes):
        self.raw = header
        self.header = self.get_header_information()
        self.raw_elements = self.get_raw_data_elements()
        self._parsed = {}

    def decode(self) -> str:
        return self.raw.decode(self.ENCODING)

    def get_header_information(self) -> str:
        return re.findall(
            self.HEADER_INFORMATION_PATTERN, self.decode(), flags=re.DOTALL
        )[0]

    def get_raw_data_elements(self) -> list:
        return re.findall(self.ELEMENT_PATTERN, self.header)[1:]

    def key_to_list(self, key: str) -> list:
        return [
            re.search(self.KEY_PATTERN, part).group()
            if re.search(self.KEY_PATTERN, part)
            else part
            for part in key.split(".")
        ]

    def split_raw_element(self, raw_element: str) -> tuple:
        tab_split = raw_element.split("\t")
        return tab_split[0], tab_split[-1]

    def parse_raw_key_and_value(self, raw_element: str) -> tuple:
        raw_key, value = self.split_raw_element(raw_element)
        key = self.key_to_list(raw_key)
        return key, value

    def search_list_pattern(self, key_part: str) -> bool:
        return re.search(self.LIST_KEY_PATTERN, key_part)

    def extract_index_from_list_match(self, list_match: re.Match) -> int:
        return int(list_match.group()[1:-1])

    def add_to_existing_element_list(
        self, part_name: str, index: int, existing_dict: list
    ) -> dict:
        try:
            existing_dict = existing_dict[part_name][index]
        except IndexError:
            existing_dict[part_name].append({})
            existing_dict = existing_dict[part_name][-1]
        return existing_dict

    def create_new_element_list(self, part_name: str, existing_dict: dict) -> dict:
        existing_dict[part_name] = [{}]
        existing_dict = existing_dict[part_name][0]
        return existing_dict

    def add_element_list_item(self):
        pass

    def scaffold_list_part(
        self, part: str, list_match: re.Match = None, existing_dict: dict = None
    ) -> dict:
        part_name = part.split("[")[0]
        list_match = list_match or self.search_list_pattern(part)
        existing_dict = existing_dict if existing_dict is not None else {}
        index = self.extract_index_from_list_match(list_match)
        existing_list = isinstance(existing_dict.get(part_name), list)
        if existing_list:
            return self.add_to_existing_element_list(part_name, index, existing_dict)
        else:
            return self.create_new_element_list(part_name, existing_dict)

    def scaffold_dict_part(self, part: str, existing_dict: dict = None) -> dict:
        existing_dict = existing_dict if existing_dict is not None else {}
        if isinstance(existing_dict.get(part), dict):
            return existing_dict[part]
        else:
            existing_dict[part] = {}
            return existing_dict[part]

    def scaffold_part(self, part: str, existing_dict: dict = None) -> dict:
        existing_dict = existing_dict if existing_dict is not None else {}
        list_match = self.search_list_pattern(part)
        if list_match:
            return self.scaffold_list_part(
                part, list_match=list_match, existing_dict=existing_dict
            )
        else:
            return self.scaffold_dict_part(part, existing_dict=existing_dict)

    def scaffold_listed_key(self, key: list, existing_dict: dict = None) -> dict:
        existing_dict = existing_dict if existing_dict is not None else {}
        for part in key[:-1]:
            existing_dict = self.scaffold_part(part, existing_dict=existing_dict)
        return existing_dict

    def assign_list_element(self, destination: dict, part: str, value):
        part_name = part.split("[")[0]
        try:
            destination[part_name].append(value)
        except (KeyError, AttributeError):
            destination[part_name] = [value]

    def assign_listed_element(self, key: list, value, destination: dict):
        part = key[-1]
        list_match = self.search_list_pattern(part)
        if list_match:
            self.assign_list_element(destination, part, value)
        else:
            destination[part] = value

    def assign_listed_key(self, key: list, value, existing_dict: dict = None):
        existing_dict = existing_dict if existing_dict is not None else {}
        destination = self.scaffold_listed_key(key, existing_dict=existing_dict)
        self.assign_listed_element(key, value, destination)

    def parse_raw_element(self, raw_element: str, existing_dict: dict = None):
        """
        Parses a raw CSA header element into the provided dictionary or creates
        a new one.

        Parameters
        ----------
        raw_element : str
            A line representing a single data element.
        existing_dict : dict
            An existing dictionary storing organized header parts.
        """

        existing_dict = existing_dict if existing_dict is not None else {}
        key, value = self.parse_raw_key_and_value(raw_element)
        return self.assign_listed_key(key, value, existing_dict=existing_dict)

    def fix_parser_elements_arg(self, raw_elements) -> list:
        elements = raw_elements or self.raw_elements
        if isinstance(elements, str):
            return [elements]
        elif not isinstance(elements, list):
            raise TypeError(
                f"The elements attribute accepts str or list values only, not {type(elements)}"  # noqa
            )
        return elements

    def parse(self, raw_elements=None):
        elements = self.fix_parser_elements_arg(raw_elements)
        parsed = {}
        for element in elements:
            self.parse_raw_element(element, existing_dict=parsed)
        return parsed
