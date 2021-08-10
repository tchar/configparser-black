from typing import Dict, Optional
from cblack.config.base import BlackConfigParser
import sys
import os
import logging
from cblack.utils.files import find_project_root

logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stderr))


class PyprojectTomlBlackConfigParser(BlackConfigParser):
    def __init__(self) -> None:
        super().__init__("pyproject.toml")

    def parse(self) -> Optional[Dict]:
        root_path = find_project_root()
        if self.filename not in os.listdir(root_path):
            return None

        filepath = root_path.joinpath(self.filename)
        with open(filepath) as f:
            for line in f:
                if line.strip() != "[tool.black]":
                    continue
                msg = "Configuration in pyproject.toml, black supports it"
                logger.warning(msg)
                return {}
        return None
