from cblack.utils.files import find_project_root
from typing import Dict, List, Optional, Union
from cblack.config.base import BlackConfigParser
import configparser
from cblack.utils.ini import clean_value


class IniBlackConfigParser(BlackConfigParser):
    def __init__(self, filename: str, black_section: str) -> None:
        super().__init__(filename)
        self.black_section = black_section

    def parse(self) -> Optional[Dict[str, Union[str, List[str]]]]:
        root_path = find_project_root()
        filepath = root_path.joinpath(self.filename)

        config = configparser.ConfigParser()
        config.read(filepath)

        if not config.has_section(self.black_section):
            return None

        conf_d = {}
        for key, value in config.items(self.black_section):
            value = value.split("\n")
            value = map(str.strip, value)
            value = filter(None, value)
            value = "".join(value)
            if value == "false":
                continue
            if value == "true":
                value = None
            else:
                value = clean_value(value)
            conf_d[key] = value
        return conf_d
