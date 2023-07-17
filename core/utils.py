import re


def remove_extra_spaces(string: str) -> str:
    return remove_extra_spaces.pattern.sub(' ', string)


remove_extra_spaces.pattern = re.compile('\s+')
