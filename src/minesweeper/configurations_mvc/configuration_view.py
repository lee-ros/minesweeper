from .. import console_utils
from .configuraion_model import (
    MAX_GRID_SIZE,
    MAX_MINES,
    ConfigurationField,
    ConfigurationModel,
)


_FIELD_TYPE_MULTIPLIER_MAP = {
    ConfigurationField.WIDTH: round(MAX_MINES / MAX_GRID_SIZE),
    ConfigurationField.HEIGHT: round(MAX_MINES / MAX_GRID_SIZE),
    ConfigurationField.MINES: 1,
}


_PRE_VALUE_BAR_FILLER = "-"
_POST_VALUE_BAR_FILLER = " "


def show_configuration_page(config: ConfigurationModel):
    _show_save_status(config.is_saved)
    for field in config.fields.values():
        is_active = field is config.active_field
        _show_field_bar(field.type, field.value, field.min, field.max, is_active)


def _show_field_bar(
    _type: ConfigurationField, value: int, _min: int, _max: int, is_active: bool
):
    bar_value = f"{value:02d}"
    if is_active:
        bar_value = console_utils.apply_graphic(
            bar_value, console_utils.ANSIGraphicsMode.RED
        )
    space_multiplier = _FIELD_TYPE_MULTIPLIER_MAP[_type]
    s = (
        f"{_type.value:>10}: "
        + f"({_min}) "
        + "["
        + _PRE_VALUE_BAR_FILLER * space_multiplier * (value - _min)
        + bar_value
        + _POST_VALUE_BAR_FILLER * space_multiplier * (_max - value)
        + "]"
        + f"({_max})"
    )

    if is_active:
        s = console_utils.apply_graphic(s, console_utils.ANSIGraphicsMode.BOLD)

    console_utils.write_line(s)


def _show_save_status(save_status: bool):
    status = "Configuration saved!\n" if save_status else "Configuration not saved!\n"
    color = (
        console_utils.ANSIGraphicsMode.GREEN
        if save_status
        else console_utils.ANSIGraphicsMode.RED
    )
    status = console_utils.apply_graphic(status, color)
    status = console_utils.apply_graphic(status, console_utils.ANSIGraphicsMode.BOLD)

    console_utils.write_line(status)
