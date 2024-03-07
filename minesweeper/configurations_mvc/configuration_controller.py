from typing import Callable, Optional, Tuple

from .configuraion_model import ConfigurationModel
from .configuration_view import show_configuration_page
from ..user_action import UserAction


class ConfigurationController:
    def __init__(self, get_config_cb: Optional[Callable] = None):
        self._configuration = ConfigurationModel()
        self._get_config_cb = get_config_cb

        self._key_action_map = {
            b"w": UserAction(
                key_visual="w",
                operation="up",
                callback=lambda: self._configuration.change_active_field(-1),
            ),
            b"s": UserAction(
                key_visual="s",
                operation="down",
                callback=lambda: self._configuration.change_active_field(1),
            ),
            b"d": UserAction(
                key_visual="d",
                operation="inc",
                callback=lambda: self._configuration.change_field(1),
            ),
            b"a": UserAction(
                key_visual="a",
                operation="dec",
                callback=lambda: self._configuration.change_field(-1),
            ),
            b"\x20": UserAction(
                key_visual="space",
                operation="save configuration",
                callback=self._handle_get_config_cb,
            ),
        }

    @property
    def help_message(self) -> str:
        """Returns the help message"""
        return UserAction.generate_help_message(self._key_action_map.values())

    def get_configuration(self) -> Tuple[int, int, int]:
        """Returns the current configuration"""
        return self._configuration.get_configuration()

    def run(self, char: Optional[bytes] = None) -> bool:
        """Runs the current controller"""
        handled = False
        action = self._key_action_map.get(char, None)
        if action:
            action.callback()
            handled = True

        show_configuration_page(self._configuration)

        return handled

    def _handle_get_config_cb(self):
        if self._get_config_cb:
            self._get_config_cb(self._configuration.get_configuration())

    def set_current_config(self, width: int, height: int, mines: int):
        """Sets the configuration to specific values"""
        self._configuration.set_configuration(width, height, mines)
