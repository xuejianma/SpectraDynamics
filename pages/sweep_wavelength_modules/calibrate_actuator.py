from threading import Thread
from utils.task import Task

class CalibrateActuatorTask(Task):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
    
    def task_loop(self):
        self.page.button_calibrate_actuator.config(state="disabled")
        try:
            self.page.actuator.calibrate()
            self.page.var_entry_curr_actuator_position.set(
                round(self.page.actuator.get_position(), 6))
        except Exception as e:
            self.page.logger.log(e)
            raise e
        finally:
            self.page.button_calibrate_actuator.config(state="normal")
            self.is_running = False