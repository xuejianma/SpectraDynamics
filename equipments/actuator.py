try:
    # thorlab_apt package from https://github.com/qpit/thorlabs_apt.
    # Sometimes this crashed the program without giving any error
    # message even with print(e). Starting thorlab's Kinesis program
    # and closing it can solve the problem. The problem came from the
    # fact that not all threads were closed when the program is closed.
    # The problem has been mostly solved with daemon=True for all worker
    # threads.
    import utils.thorlabs_apt as apt
except:
    pass
from time import sleep


class Actuator:
    def __init__(self, id_string_var=None):
        self.valid = False
        self.error_message = ""
        try:
            if id_string_var:
                serial_number = int(id_string_var.get())
            else:
                serial_number = 27264119
            self.motor = apt.Motor(serial_number)
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error_message = e

    def get_position(self):
        return self.motor.position

    def set_position(self, position):
        self.motor.move_to(position)
        while self.motor.is_in_motion:
            sleep(0.1)

    def home(self):
        self.motor.move_home()
        while self.motor.is_in_motion:
            sleep(0.1)


class ActuatorSimulator:
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""
        self.position = 0

    def get_position(self):
        return self.position

    def set_position(self, position):
        sleep(1)
        self.position = position

    def home(self):
        sleep(1)
        self.position = 0
