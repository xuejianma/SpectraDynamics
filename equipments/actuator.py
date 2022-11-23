try:
    # thorlab_apt package from https://github.com/qpit/thorlabs_apt.
    # Sometimes this will crash the program without giving any error
    # message even with print(e). Starting thorlab's Kinesis program 
    # and closing it can solve the problem.
    import utils.thorlabs_apt as apt
except:
    pass
from time import sleep


class Actuator:
    def __init__(self, serial_number=27264119):
        self.valid = False
        self.error_message = ""
        try:
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


class ActuatorSimulator:
    def __init__(self):
        self.valid = True
        self.error_message = ""
        self.position = 0

    def get_position(self):
        return self.position

    def set_position(self, position):
        sleep(1)
        self.position = position
