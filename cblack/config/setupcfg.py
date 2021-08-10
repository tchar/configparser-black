from cblack.config.ini import IniBlackConfigParser


class SetupCfgBlackConfigParser(IniBlackConfigParser):
    def __init__(self) -> None:
        super().__init__("setup.cfg", "tool:black")
