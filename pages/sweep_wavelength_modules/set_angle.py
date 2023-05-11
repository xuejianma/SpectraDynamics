from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER

class SetAngleTask():
    def __init__(self, button_set_angle) -> None:
        self.is_running = False
        self.button_set_angle = button_set_angle
        self.external_button_control = False

    def task_loop(self):
        if not self.external_button_control:
            self.button_set_angle.config(state="disabled")
        try:
            for angle in INSTANCES.ndfilter.set_angle(
                    float(VARIABLES.var_spinbox_target_angle.get())):
                VARIABLES.var_entry_curr_angle.set(round(angle, 6))
            VARIABLES.var_entry_curr_angle.set(
                round(INSTANCES.ndfilter.get_angle(), 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if not self.external_button_control:
                self.button_set_angle.config(state="normal")
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()