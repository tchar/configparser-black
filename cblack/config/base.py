from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union


class BlackConfigParser(ABC):
    def __init__(self, filename: str) -> None:
        self.filename = filename

    @abstractmethod
    def parse(self) -> Optional[Dict[str, Union[str, List[str]]]]:
        pass
