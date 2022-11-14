import utils.thorlabs_apt as apt # thorlab_apt package from https://github.com/qpit/thorlabs_apt
from time import sleep
# from utils.config import VARIABLES


class NDFilter:
    def __init__(self, serial_number = 55254094):
        try:
            self.motor = apt.Motor(serial_number)
        except Exception as e:
            print(e)
    def get_angle(self):
        return self.motor.position
    def set_angle(self):
        # prev_angle = self.ndfilter_controller.get_angle()
        self.ndfilter_controller.motor.move_to(self.angle)
        while self.ndfilter_controller.motor.is_in_motion:
            sleep(0.1)
        #     sleep(0.1)
        #     curr_angle = self.ndfilter_controller.get_angle()
        #     self.progress = int((curr_angle - prev_angle) / (self.angle - prev_angle) * 100) if self.angle != prev_angle else 0
        # self.progress = 100

class NDFilterSimulator:
    def __init__(self):
        self.angle = 0
    def get_angle(self):
        return self.angle
    def set_angle(self, angle):
        sleep(1)
        self.angle = angle