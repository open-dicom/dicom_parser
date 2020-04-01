from pydicom.tag import Tag as PydicomTag


def int_to_tag_hex(value: int) -> str:
    return format(value, "x").zfill(4)


def parse_tag(tag: PydicomTag) -> tuple:
    return int_to_tag_hex(tag.group), int_to_tag_hex(tag.element)
