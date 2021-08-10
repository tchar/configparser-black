import re
from typing import List


def pretty_args(args: List[str]) -> List[str]:
    sl = []
    for arg in args:
        if arg.startswith("-") or re.match(r"^\s*[a-zA-Z0-9]+\s*$", arg):
            sl.append(arg)
            continue
        arg = arg.replace('"', '\\"')
        arg = '"{}"'.format(arg)
        sl.append(arg)
    return sl
