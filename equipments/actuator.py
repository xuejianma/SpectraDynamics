try:
    import utils.thorlabs_apt as apt # thorlab_apt package from https://github.com/qpit/thorlabs_apt
except:
    pass
from time import sleep

class Actuator:
    def __init__(self, serial_number = 27264119):
        try:
            self.motor = apt.Motor(serial_number)
        except Exception as e:
            print(e)
    def get_position(self):
        return self.motor.position
    def set_position(self, position):
        self.motor.move_to(position)
        while self.motor.is_in_motion:
            sleep(0.1)

class ActuatorSimulator:
    def __init__(self):
        self.position = 0
    def get_position(self):
        return self.position
    def set_position(self, position):
        sleep(1)
        self.position = position