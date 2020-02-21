import re


class CsaHeader:
    ENCODING = "ISO-8859-1"
    HEADER_INFORMATION_PATTERN = r"### ASCCONV BEGIN(.*)### ASCCONV END ###"
    ELEMENT_PATTERN = r"([A-Z][^\n]*)"
    KEY_PATTERN = r"([A-Z][\w]*[^\.\t\[])"
    GROUP_PATTERN = r"[a-z]??({key}[.]*)"

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

    def get_raw_group(self, key: str, from_group: list = None) -> list:
        from_group = from_group or self.raw_elements
        return [
            re.search(self.ELEMENT_PATTERN, ".".join(element.split(".")[1:])).group()
            for element in from_group
            if re.search(self.GROUP_PATTERN.format(key=key), element)
        ]

    def get_raw_group_keys(self, raw_group: list) -> set:
        return set(
            [re.search(self.KEY_PATTERN, element).group() for element in raw_group]
        )

    def parse_raw_element(self, key: list, value: str):
        parsed_destination = self._parsed
        for part in key[:-1]:
            list_element = re.search(r"\[\d+\]", part)
            if list_element:
                index = int(list_element.group()[1:-1])
                list_key = part.split("[")[0]
                if isinstance(parsed_destination.get(list_key), list):
                    try:
                        parsed_destination = parsed_destination[list_key][index]
                    except IndexError:
                        parsed_destination[list_key].append({})
                        parsed_destination = parsed_destination[list_key][-1]
                else:
                    parsed_destination[list_key] = [{}]
                    parsed_destination = parsed_destination[list_key][0]
            else:
                if isinstance(parsed_destination.get(part), dict):
                    parsed_destination = parsed_destination[part]
                else:
                    parsed_destination[part] = {}
                    parsed_destination = parsed_destination[part]
        part = key[-1]
        list_element = re.search(r"\[\d+\]", part)
        if list_element:
            list_key = part.split("[")[0]
            try:
                parsed_destination[list_key].append(value)
            except (KeyError, AttributeError):
                parsed_destination[list_key] = [value]
        else:
            parsed_destination[part] = value

    def parse(self):
        for element in self.raw_elements:
            tab_split = element.split("\t")
            key, value = tab_split[0], tab_split[-1]
            if "__" not in key:
                key = key.split(".")
                key = [
                    re.search(r"[A-Z].*", part).group()
                    if re.search(r"[A-Z].*", part)
                    else part
                    for part in key
                ]
                self.parse_raw_element(key, value)
