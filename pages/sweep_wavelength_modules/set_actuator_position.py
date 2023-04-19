from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER

class SetActuatorPositionTask():
    def __init__(self, button_set_actuator_position) -> None:
        self.is_running = False
        self.button_set_actuator_position = button_set_actuator_position
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_actuator_position.config(state="disabled")
        try:
            INSTANCES.actuator.set_position(
                float(VARIABLES.var_spinbox_target_actuator_position.get()))
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_actuator_position.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()