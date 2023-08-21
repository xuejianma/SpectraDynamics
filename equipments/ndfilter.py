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
from equipments.powermeter import MAX_PERIOD


class NDFilter:
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

    def get_angle(self):
        return self.motor.position

    def set_angle(self, angle):
        self.motor.move_to(angle)
        while self.motor.is_in_motion:
            sleep(MAX_PERIOD)
            yield self.get_angle()
    
    def set_angle_direct(self, angle):
        self.motor.move_to(angle)
        while self.motor.is_in_motion:
            sleep(MAX_PERIOD)
    
    def home(self):
        self.motor.move_home()
        while self.motor.is_in_motion:
            sleep(MAX_PERIOD)


class NDFilterSimulator:
    def __init__(self, *args, **kwargs):
        self.valid = True
        self.error_message = ""
        self.angle = 0

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        direction = 1 if angle > self.angle else -1
        curr_angle = self.angle
        delta = 1 * MAX_PERIOD / 0.1
        steps = int(abs(angle - curr_angle) / delta)
        for _ in range(steps):
            self.angle += delta * direction
            sleep(MAX_PERIOD)
            yield self.get_angle()
        self.angle = angle
    
    def home(self):
        sleep(1)
        self.angle = 0
        

