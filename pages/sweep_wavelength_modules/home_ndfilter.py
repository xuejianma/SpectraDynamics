from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER

class HomeNDFilterTask():
    def __init__(self, button_home_ndfilter) -> None:
        self.is_running = False
        self.button_home_ndfilter = button_home_ndfilter
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_home_ndfilter.config(state="disabled")
        try:
            INSTANCES.ndfilter.home()
            VARIABLES.var_entry_curr_angle.set(
                round(INSTANCES.ndfilter.get_angle(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_home_ndfilter.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()