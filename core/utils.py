import re


spaces_pattern = re.compile('\s+')


def remove_extra_spaces(string: str) -> str:
    return spaces_pattern.sub(' ', string)
