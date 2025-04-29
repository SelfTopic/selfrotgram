import configparser
from typing import Union
import os

class CfgParser:

    path: str = None
    parser: configparser.ConfigParser

    def __init__(self, path_cfg: str = 'bot_cfg.cfg'):
        self.path = path_cfg
        self.parser = configparser.ConfigParser()
        
    def create_config(self):
        self.parser['DEFAULT'] = {'bot_token': 'YOUR_BOT_TOKEN'}  
        with open(self.path, 'w') as cfg:
            self.parser.write(cfg)

    def read_config(self):
        try:
            self.parser.read(self.path)
        except Exception as e:
            print(f"Error configure: {e}")

    def get(self, key: str) -> Union[str, None]:
        try:
            return self.parser.get(section='DEFAULT', option=key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return None 
