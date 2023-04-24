from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER

class HomeActuatorTask():
    def __init__(self, button_home_actuator) -> None:
        self.is_running = False
        self.button_home_actuator = button_home_actuator
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_home_actuator.config(state="disabled")
        try:
            INSTANCES.actuator.home()
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_home_actuator.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()