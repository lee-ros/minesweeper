from minesweeper.controller_runner import ControllerRunner
from minesweeper.game_mvc import GameController


if __name__ == "__main__":
    game_controller = GameController()
    controller_runner = ControllerRunner(game_controller)
    controller_runner.run()
