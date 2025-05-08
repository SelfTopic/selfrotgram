from typing import Union, Self
from .menu_button_default import MenuButtonDefault
from .menu_button_web_app import MenuButtonWebApp
from .menu_button_commands import MenuButtonCommands

MenuButton = Union[MenuButtonCommands, MenuButtonWebApp, MenuButtonDefault]