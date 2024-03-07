from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, List


@dataclass
class UserAction:
    """Dataclass that defines the user action interface for handling input

    Help messages auto generator use this class
    """

    key_visual: str
    operation: str
    callback: Callable

    @staticmethod
    def generate_help_message(actions: List["UserAction"]):
        keys_by_type = defaultdict(lambda: [])

        for action in actions:
            keys_by_type[action.operation].append(action.key_visual)

        msgs = []
        for action_type, keys in keys_by_type.items():
            action_keys = "/".join(keys)
            msgs.append(f"({action_keys}) - {action_type}")

        return ", ".join(msgs)
