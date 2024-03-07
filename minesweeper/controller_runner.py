import msvcrt
import time

from .controller import Controller


class ControllerRunner:
    """MVC Controller runner class
    
    Handles input reading
    """
    def __init__(self, controller: Controller):
        self._controller = controller

    def run(self):
        inp = None
        while True:
            if msvcrt.kbhit():
                inp = msvcrt.getch()
            else:
                inp = None
                time.sleep(0.05)

            self._controller.run(inp)
