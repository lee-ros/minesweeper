from dataclasses import dataclass
from enum import Enum
from typing import Dict, Literal, Tuple, Union


IntOnlyOne = Union[Literal[1], Literal[0], Literal[-1]]

DEFAULT_GRID_SIZE = 10
MAX_GRID_SIZE = 50
MIN_GRID_SIZE = 5

DEFAULT_MINES = 10
MAX_MINES = 99
MIN_MINES = 5


class ConfigurationField(Enum):
    """Configuration fields"""

    WIDTH = "Width"
    HEIGHT = "Height"
    MINES = "Mines"


@dataclass
class Field:
    type: ConfigurationField
    value: int
    min: int
    max: int


class ConfigurationModel:
    def __init__(self):
        self._fields = {
            ConfigurationField.WIDTH: Field(
                ConfigurationField.WIDTH,
                DEFAULT_GRID_SIZE,
                MIN_GRID_SIZE,
                MAX_GRID_SIZE,
            ),
            ConfigurationField.HEIGHT: Field(
                ConfigurationField.HEIGHT,
                DEFAULT_GRID_SIZE,
                MIN_GRID_SIZE,
                MAX_GRID_SIZE,
            ),
            ConfigurationField.MINES: Field(
                ConfigurationField.MINES, DEFAULT_MINES, MIN_MINES, MAX_MINES
            ),
        }

        self._is_saved = True

        self._active_field: Field = None
        self._active_field_index = 0
        self.change_active_field(0)

    @property
    def fields(self) -> Dict[ConfigurationField, Field]:
        """Returns a dictionary of (field, value) for the current config"""
        return self._fields

    @property
    def active_field(self) -> Field:
        """Returns the active field"""
        return self._active_field

    @property
    def is_saved(self) -> bool:
        """Returns if the current config was saved from the last edit"""
        return self._is_saved

    def get_configuration(self) -> Tuple[int, int, int]:
        """Returns the current configuration `(width, height, mines)`"""
        self._is_saved = True
        width = self._fields[ConfigurationField.WIDTH].value
        height = self._fields[ConfigurationField.HEIGHT].value
        mines = self._fields[ConfigurationField.MINES].value
        return width, height, mines
    
    def set_configuration(self, width: int, height: int, mines: int):
        """Sets the model configuration to specific values"""
        self._fields[ConfigurationField.WIDTH].value = width
        self._fields[ConfigurationField.HEIGHT].value = height
        self._fields[ConfigurationField.MINES].value = mines

    def change_active_field(self, direction: IntOnlyOne):
        """Change the active field being edited

        If `direction == 1` move to the next field.
        If `direction == -1` move to the previous field
        """
        self._active_field_index += direction
        self._active_field_index %= len(self._fields.keys())
        self._active_field = [*self._fields.values()][self._active_field_index]

    def change_field(self, offset: int):
        """Changes the value of the active field by `offset`"""
        self._increment_field(self._active_field, offset)
        self._set_mines_max_value()
        self._increment_field(self._fields[ConfigurationField.MINES], 0)
        self._is_saved = False

    def _set_mines_max_value(self):
        mines_field = self._fields[ConfigurationField.MINES]
        width_field = self._fields[ConfigurationField.WIDTH]
        height_field = self._fields[ConfigurationField.HEIGHT]

        max_mines_possible = int(width_field.value * height_field.value)
        max_mines_allowed = min(MAX_MINES, max_mines_possible)
        mines_field.max = max_mines_allowed

    def _increment_field(self, field: Field, offset: int):
        new_value = field.value + offset

        if new_value > field.max:
            new_value = field.max
        elif new_value < field.min:
            new_value = field.min

        field.value = new_value
