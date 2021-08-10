from cblack.config.ini import IniBlackConfigParser


class ToxIniBlackConfigParser(IniBlackConfigParser):
    def __init__(self) -> None:
        super().__init__("tox.ini", "black")
