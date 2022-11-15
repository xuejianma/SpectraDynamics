from tkinter import ttk
from utils.config import INSTANCES, VARIABLES, LOGGER
from utils.spinbox import Spinbox
from utils.plot import Plot
from utils.task import Task
from utils.save import Save
from threading import Thread
from time import sleep


class SweepWavelength:
    def __init__(self, parent) -> None:
        self.frame, button_set_angle, button_set_wavelength, button_set_actuator_position, \
            self.button_power, spinbox_sweep_start_wavelength, spinbox_sweep_end_wavelength, \
            spinbox_sweep_step_size, frame_1_5 = self.set_frame(parent)
        self.set_angle_task = SetAngleTask(button_set_angle)
        self.read_power_task = ReadPowerTask(self.button_power)
        self.set_wavelength_task = SetWavelengthTask(button_set_wavelength)
        self.set_actuator_position_task = SetActuatorPositionTask(
            button_set_actuator_position)
        SweepWavelengthTask(frame_1_5, spinbox_sweep_start_wavelength,
                            spinbox_sweep_end_wavelength, spinbox_sweep_step_size, self.set_wavelength_task)

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_2 = ttk.Frame(frame)
        frame_2.pack(side="top", padx=10, pady=10)
        frame_3 = ttk.Frame(frame)
        frame_3.pack(side="top", padx=10, pady=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", anchor="n", padx=10, pady=10)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", anchor="n", padx=10, pady=10)
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", anchor="n", padx=10, pady=10)
        frame_1_4 = ttk.Frame(frame_1)
        frame_1_4.pack(side="left", anchor="n", padx=10, pady=10)
        frame_1_5 = ttk.Frame(frame_1)
        frame_1_5.pack(side="left", anchor="n", padx=10, pady=10)
        frame_1_6 = ttk.Frame(frame_1)
        frame_1_6.pack(side="left", anchor="n", padx=10, pady=10)
        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack(side="left", anchor="n", padx=10, pady=10)
        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack(side="left", anchor="n", padx=10, pady=10)
        frame_3_1 = ttk.Frame(frame_3)
        frame_3_1.pack(side="left", anchor="n", padx=10, pady=10)
        frame_3_2 = ttk.Frame(frame_3)
        frame_3_2.pack(side="left", anchor="n", padx=10, pady=10)
        label_wavelength = ttk.Label(
            frame_1_1, text="Current Wavelength (nm):")
        label_wavelength.pack(side="top", anchor="w")
        entry_wavelength = ttk.Entry(
            frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_curr_wavelength)
        entry_wavelength.pack(side="top", anchor="w")
        label_wavelength = ttk.Label(frame_1_1, text="Target Wavelength (nm):")
        label_wavelength.pack(side="top", anchor="w")
        spinbox_wavelength = Spinbox(frame_1_1, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_target_wavelength)
        spinbox_wavelength.pack(side="top", anchor="w")
        button_set_wavelength = ttk.Button(
            frame_1_1, text="Set Wavelength", command=self.on_set_wavelength)
        button_set_wavelength.pack(side="top", anchor="w")
        label_angle = ttk.Label(
            frame_1_2, text="Current NDFilter Rotation Angle (deg): ")
        label_angle.pack(side="top", anchor="w")
        entry_angle = ttk.Entry(
            frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_angle)
        entry_angle.pack(side="top", anchor="w")
        label_set_angle = ttk.Label(frame_1_2, text="Target Angle (deg): ")
        label_set_angle.pack(side="top", anchor="w")
        spinbox_set_angle = Spinbox(
            frame_1_2, from_=0, to=360, increment=0.1, textvariable=VARIABLES.var_spinbox_target_angle)
        spinbox_set_angle.pack(side="top", anchor="w")
        button_set_angle = ttk.Button(
            frame_1_2, text="Set Angle", command=self.on_set_angle)
        button_set_angle.pack(side="top", anchor="w")
        label_power = ttk.Label(frame_1_3, text="Current Power (uW): ")
        label_power.pack(side="top", anchor="w")
        entry_power = ttk.Entry(
            frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_power)
        entry_power.pack(side="top", anchor="w")
        button_power = ttk.Button(
            frame_1_3, text="Turn ON", command=self.toggle_power)
        button_power.pack(side="top", anchor="w")
        label_actuator_position = ttk.Label(
            frame_1_4, text="Actuator Position (mm): ")
        label_actuator_position.pack(side="top", anchor="w")
        entry_actuator_position = ttk.Entry(
            frame_1_4, state="readonly", textvariable=VARIABLES.var_entry_curr_actuator_position)
        entry_actuator_position.pack(side="top", anchor="w")
        label_set_actuator_position = ttk.Label(
            frame_1_4, text="Target Actuator Position (mm): ")
        label_set_actuator_position.pack(side="top", anchor="w")
        spinbox_set_actuator_position = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_target_actuator_position)
        spinbox_set_actuator_position.pack(side="top", anchor="w")
        button_set_actuator_position = ttk.Button(
            frame_1_4, text="Set Position", command=self.on_set_actuator_position)
        button_set_actuator_position.pack(side="top", anchor="w")
        label_sweep_start_wavelength = ttk.Label(
            frame_1_5, text="Sweep Start Wavelength (nm): ")
        label_sweep_start_wavelength.pack(side="top", anchor="w")
        spinbox_sweep_start_wavelength = Spinbox(frame_1_5, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_start_wavelength)
        spinbox_sweep_start_wavelength.pack(side="top", anchor="w")
        label_sweep_end_wavelength = ttk.Label(
            frame_1_5, text="Sweep End Wavelength (nm): ")
        label_sweep_end_wavelength.pack(side="top", anchor="w")
        spinbox_sweep_end_wavelength = Spinbox(frame_1_5, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_end_wavelength)
        spinbox_sweep_end_wavelength.pack(side="top", anchor="w")
        label_sweep_step_size = ttk.Label(
            frame_1_5, text="Sweep Step Size (nm): ")
        label_sweep_step_size.pack(side="top", anchor="w")
        spinbox_sweep_step_size = Spinbox(frame_1_5, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_step_size)
        spinbox_sweep_step_size.pack(side="top", anchor="w")

        plot_lifetime_instant_ch1 = Plot(frame_2_1)
        plot_lifetime_average_ch1 = Plot(frame_2_2)
        plot_lifetime_instant_ch2 = Plot(frame_3_1)
        plot_lifetime_average_ch2 = Plot(frame_3_2)
        return frame, button_set_angle, button_set_wavelength, button_set_actuator_position, button_power, spinbox_sweep_start_wavelength, spinbox_sweep_end_wavelength, spinbox_sweep_step_size, frame_1_5

    def toggle_power(self):
        if self.read_power_task.is_running:
            self.button_power.config(state="disabled")
            self.read_power_task.terminate()
            self.button_power["text"] = "Turn ON"
        else:
            self.read_power_task.start()
            self.button_power["text"] = "Turn OFF"

    def on_set_angle(self):
        self.set_angle_task.start()

    def on_set_wavelength(self):
        self.set_wavelength_task.start()

    def on_set_actuator_position(self):
        self.set_actuator_position_task.start()


class SetAngleTask():
    def __init__(self, button_set_angle) -> None:
        self.button_set_angle = button_set_angle

    def task_loop(self):
        self.button_set_angle.config(state="disabled")
        try:
            INSTANCES.ndfilter.set_angle(
                float(VARIABLES.var_spinbox_target_angle.get()))
            VARIABLES.var_entry_curr_angle.set(
                round(INSTANCES.ndfilter.get_angle(), 4))
        except Exception as e:
            LOGGER.log(e)
        self.button_set_angle.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class ReadPowerTask():
    def __init__(self, button_power) -> None:
        self.is_running = False
        self.button_power = button_power

    def task_loop(self):
        try:
            while self.is_running:
                power_sum = 0
                for _ in range(5):
                    power_sum += INSTANCES.powermeter.get_power_uW()
                    sleep(0.1)
                VARIABLES.var_entry_curr_power.set(power_sum / 5)
        except Exception as e:
            LOGGER.log(e)
        self.button_power.config(state="normal")

    def start(self):
        self.is_running = True
        thread = Thread(target=self.task_loop)
        thread.start()

    def terminate(self):
        self.is_running = False


class SetWavelengthTask():
    def __init__(self, button_set_wavelength) -> None:
        self.button_set_wavelength = button_set_wavelength

    def task_loop(self):
        self.button_set_wavelength.config(state="disabled")
        try:
            INSTANCES.monochromator.set_wavelength(
                float(VARIABLES.var_spinbox_target_wavelength.get()))
            VARIABLES.var_entry_curr_wavelength.set(
                round(INSTANCES.monochromator.get_wavelength(), 4))
        except Exception as e:
            LOGGER.log(e)
        self.button_set_wavelength.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class SetActuatorPositionTask():
    def __init__(self, button_set_actuator_position) -> None:
        self.button_set_actuator_position = button_set_actuator_position

    def task_loop(self):
        self.button_set_actuator_position.config(state="disabled")
        try:
            INSTANCES.actuator.set_position(
                float(VARIABLES.var_spinbox_target_actuator_position.get()))
            VARIABLES.var_entry_curr_actuator_position.set(
                round(INSTANCES.actuator.get_position(), 4))
        except Exception as e:
            LOGGER.log(e)
        self.button_set_actuator_position.config(state="normal")

    def start(self):
        thread = Thread(target=self.task_loop)
        thread.start()


class SweepWavelengthTask(Task):
    def __init__(self, parent, spinbox_sweep_start_wavelength, spinbox_sweep_end_wavelength, spinbox_sweep_step_size, set_wavelength_task) -> None:
        super().__init__(parent)
        self.spinbox_sweep_start_wavelength = spinbox_sweep_start_wavelength
        self.spinbox_sweep_end_wavelength = spinbox_sweep_end_wavelength
        self.spinbox_sweep_step_size = spinbox_sweep_step_size
        self.start_wavelength = float(
            VARIABLES.var_spinbox_sweep_start_wavelength.get())
        self.end_wavelength = float(
            VARIABLES.var_spinbox_sweep_end_wavelength.get())
        self.step_size = float(VARIABLES.var_spinbox_sweep_step_size.get())
        self.curr_wavelength = self.start_wavelength

    def task(self):
        pass
        # start_wavelength = float(self.spinbox_sweep_start_wavelength.get())
        # end_wavelength = float(self.spinbox_sweep_end_wavelength.get())
        # step_size = float(self.spinbox_sweep_step_size.get())
        # if start_wavelength > end_wavelength:
        #     start_wavelength, end_wavelength = end_wavelength, start_wavelength
        # for wavelength in np.arange(start_wavelength, end_wavelength, step_size):
        #     INSTANCES.monochromator.set_wavelength(wavelength)
        #     VARIABLES.var_entry_curr_wavelength.set(
        #         round(INSTANCES.monochromator.get_wavelength(), 4))
        #     sleep(0.1)

    def start(self):
        self.num = int(float(VARIABLES.var_spinbox_sweep_end_wavelength.get()) - float(
            VARIABLES.var_spinbox_sweep_start_wavelength.get())) / float(VARIABLES.var_spinbox_sweep_step_size.get())
        self.spinbox_sweep_start_wavelength.config(state="disabled")
        self.spinbox_sweep_end_wavelength.config(state="disabled")
        self.spinbox_sweep_step_size.config(state="disabled")
        super().start()

    def reset(self):
        super().reset()
        self.spinbox_sweep_start_wavelength.config(state="normal")
        self.spinbox_sweep_end_wavelength.config(state="normal")
        self.spinbox_sweep_step_size.config(state="normal")

    # def task_loop(self):
    #     self.button_sweep_wavelength.config(state="disabled")
    #     try:
    #         start_wavelength = float(VARIABLES.var_spinbox_sweep_start_wavelength.get())
    #         end_wavelength = float(VARIABLES.var_spinbox_sweep_end_wavelength.get())
    #         step_size = float(VARIABLES.var_spinbox_sweep_step_size.get())
    #         INSTANCES.monochromator.set_wavelength(start_wavelength)
    #         VARIABLES.var_entry_curr_wavelength.set(round(INSTANCES.monochromator.get_wavelength(), 4))
    #         for wavelength in np.arange(start_wavelength, end_wavelength, step_size):
    #             INSTANCES.monochromator.set_wavelength(wavelength)
    #             VARIABLES.var_entry_curr_wavelength.set(round(INSTANCES.monochromator.get_wavelength(), 4))
    #             sleep(0.1)
    #     except Exception as e:
    #         LOGGER.log(e)
    #     self.button_sweep_wavelength.config(state="normal")
    # def start(self):
    #     thread = Thread(target=self.task_loop)
    #     thread.start()
