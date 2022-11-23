try:
    # thorlab_apt package from https://github.com/qpit/thorlabs_apt.
    # Sometimes this will crash the program without giving any error
    # message even with print(e). Starting thorlab's Kinesis program 
    # and closing it can solve the problem.
    import utils.thorlabs_apt as apt
except:
    pass
from time import sleep


class NDFilter:
    def __init__(self, serial_number=55254094):
        self.valid = False
        self.error_message = ""
        try:
            self.motor = apt.Motor(serial_number)
            self.valid = True
        except Exception as e:
            self.valid = False
            self.error_message = e

    def get_angle(self):
        return self.motor.position

    def set_angle(self, angle):
        self.motor.move_to(angle)
        while self.motor.is_in_motion:
            sleep(0.1)


class NDFilterSimulator:
    def __init__(self):
        self.valid = True
        self.error_message = ""
        self.angle = 0

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        sleep(1)
        self.angle = angle
