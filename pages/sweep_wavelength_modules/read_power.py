from threading import Thread
from utils.config import VARIABLES, INSTANCES, LOGGER

class ReadPowerTask():
    def __init__(self, button_power) -> None:
        self.is_running = False
        self.button_power = button_power

    def task_loop(self):
        try:
            # sometimes the powermeter will have VisaIOError and rerunning the command will fix it.
            while self.is_running:
                count = 0
                max_try = 10
                error = None
                while count < max_try:
                    try:
                        power = INSTANCES.powermeter.get_power_uW()
                        break
                    except Exception as e:
                        error = e
                        count += 1
                if count == max_try:
                    raise error
                background_power = float(
                    VARIABLES.var_spinbox_background_power.get())
                VARIABLES.var_entry_curr_power.set(
                    round(power - background_power, 6))
        except Exception as e:
            LOGGER.log(e)
            raise e
        finally:
            if self.button_power["text"] == "Turn OFF":
                self.button_power["text"] = "Turn ON"
            self.button_power.config(state="normal")
            # Set is_running to False here in case the stopping comes from error and self.terminate() is not called.
            self.is_running = False

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.setDaemon(True)
        thread.start()

    def terminate(self):
        self.is_running = False