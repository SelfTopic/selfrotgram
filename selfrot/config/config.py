from .parser import CfgParser
from typing import Optional
import os

class ConfigAPI:

    token: str
    parser: CfgParser

    def __init__(self, path_cfg: str = 'bot_cfg.cfg'):

        self.parser = CfgParser(path_cfg=path_cfg)
        filenames = os.listdir()
        if path_cfg not in filenames:
            self.parser.create_config()  
        self.parser.read_config()

    def get_token(self, key: str = 'bot_token') -> Optional[str]:
        token = self.parser.get(key=key)
        print(token)
        return token