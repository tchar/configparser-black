from ast import literal_eval
from typing import Union, List


def clean_value(value: str) -> Union[str, List[str]]:
    try:
        possible_list = literal_eval(value)
        if not isinstance(possible_list, list):
            raise Exception("Not a list")
        possible_list = map(str, possible_list)
        value = list(possible_list)
        return value
    except Exception:
        pass
    lvalue = value.lstrip('"')
    if lvalue == value:
        lvalue = value.lstrip("'")
    value = lvalue
    rvalue = value.rstrip('"')
    if rvalue == value:
        rvalue = value.rstrip("'")
    value = rvalue
    return value
