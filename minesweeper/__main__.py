from .controller_runner import ControllerRunner
from .game_mvc import GameController


def main():
    game_controller = GameController()
    controller_runner = ControllerRunner(game_controller)
    controller_runner.run()
