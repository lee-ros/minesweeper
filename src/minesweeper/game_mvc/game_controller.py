from typing import Optional, Tuple
from ..board_mvc import BoardController
from ..configurations_mvc import ConfigurationController
from ..controller import Controller
from ..user_action import UserAction
from .game_view import show_game_help_bar


_DEFAULT_CONFIG = (10, 10, 10)


class GameController:
    def __init__(self):
        self._config = _DEFAULT_CONFIG
        self._config_updated = False

        self._config_controller = ConfigurationController(self._update_config)
        self._config_controller.set_current_config(*_DEFAULT_CONFIG)

        self._board_controller = BoardController()
        self._board_controller.create_new_board(*_DEFAULT_CONFIG)

        self._active_controller = self._board_controller

        self._key_action_map = {
            b"o": UserAction(
                key_visual="o",
                operation="open/close Settings",
                callback=self._open_close_settings,
            ),
            b"\x1b": UserAction(key_visual="Esc", operation="exit", callback=exit),
        }

    @property
    def help_message(self) -> str:
        """Returns the help message"""
        return ", ".join(
            [
                self._active_controller.help_message,
                UserAction.generate_help_message(self._key_action_map.values()),
            ]
        )

    def run(self, char: Optional[bytes] = None) -> bool:
        """Runs the current controller"""
        show_game_help_bar(self.help_message)

        if self._config_updated:
            self._handle_new_config()

        handled = self._active_controller.run(char)

        action = self._key_action_map.get(char, None)
        if action:
            action.callback()
            handled = True

        return handled

    def _handle_new_config(self):
        self._config_updated = False
        self._board_controller.create_new_board(*self._config)
        self._active_controller = self._board_controller

    def _set_active_controller(self, controller: Controller):
        self._active_controller = controller
        self.run()

    def _update_config(self, config: Tuple[int, int, int]):
        self._config = config
        self._config_updated = True

    def _open_close_settings(self):
        if self._active_controller is self._board_controller:
            self._set_active_controller(self._config_controller)
        elif self._active_controller is self._config_controller:
            self._set_active_controller(self._board_controller)
