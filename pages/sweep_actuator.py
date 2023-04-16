import tkinter as tk
from tkinter import ttk
from utils.spinbox import Spinbox
from utils.task import Task, PAUSED
from utils.plot import Plot
from utils.save import Save
from utils.config import VARIABLES, LOGGER, INSTANCES


class SweepActuator:
    '''
    For each wavelength, sweep actuator positions around the current position 
    to find the maximum power. Record the optimal actuator positions for 
    wanted wavelengths. Save them in a csv file for future use.
    '''
    def __init__(self, parent):
        self.frame = self.set_frame(parent)

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        # frame_1 = ttk.Frame(frame)
        # frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        # frame_2 = ttk.Frame(frame)
        # frame_2.pack(side="top", padx=10)
        # frame_3 = ttk.Frame(frame)
        # frame_3.pack(side="top", padx=10, pady=10)
        # frame_1_1 = ttk.Frame(frame_1)
        # frame_1_1.pack(side="left", anchor="n", padx=10)
        # frame_1_2 = ttk.Frame(frame_1)
        # frame_1_2.pack(side="left", anchor="n", padx=10)
        # frame_1_3 = ttk.Frame(frame_1)
        # frame_1_3.pack(side="left", anchor="n", padx=10)
        # frame_1_4 = ttk.Frame(frame_1)
        # frame_1_4.pack(side="left", anchor="n", padx=10)
        # frame_1_5 = ttk.Frame(frame_1)
        # frame_1_5.pack(side="left", anchor="n", padx=10)
        # frame_1_6 = ttk.Frame(frame_1)
        # frame_1_6.pack(side="left", anchor="n", padx=10)
        # frame_1_7 = ttk.Frame(frame_1)
        # frame_1_7.pack(side="left", anchor="n", padx=10)
        # frame_2_1 = ttk.Frame(frame_2)
        # frame_2_1.pack(side="left", anchor="n", padx=10)
        # frame_2_2 = ttk.Frame(frame_2)
        # frame_2_2.pack(side="left", anchor="n", padx=10)
        # frame_3_1 = ttk.Frame(frame_3)
        # frame_3_1.pack(side="left", anchor="n", padx=10)
        # frame_3_2 = ttk.Frame(frame_3)
        # frame_3_2.pack(side="left", anchor="n", padx=10)
        # ttk.Label(frame_1_1, text="Current Wavelength (nm):").pack(
        #     side="top", anchor="w")
        # ttk.Entry(frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_curr_wavelength).pack(
        #     side="top", anchor="w")
        # ttk.Label(frame_1_1, text="Target Wavelength (nm):").pack(
        #     side="top", anchor="w")
        # self.spinbox_target_wavelength = Spinbox(frame_1_1, from_=0, to=float("inf"),
        #                                          textvariable=VARIABLES.var_spinbox_target_wavelength)
        # self.spinbox_target_wavelength.pack(side="top", anchor="w")
        # self.button_set_wavelength = ttk.Button(
        #     frame_1_1, text="Set Wavelength", command=self.on_set_wavelength)
        # self.button_set_wavelength.pack(side="top", anchor="w")
        # ttk.Label(frame_1_2, text="Actuator Position (mm): ").pack(
        #     side="top", anchor="w")
        # ttk.Entry(frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_actuator_position).pack(
        #     side="top", anchor="w")
        # ttk.Label(frame_1_2, text="Target Actuator Position (mm): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_target_actuator_position = Spinbox(frame_1_2, from_=0, to=float("inf"), increment=0.01,
        #                                                 textvariable=VARIABLES.var_spinbox_target_actuator_position)
        # self.spinbox_target_actuator_position.pack(side="top", anchor="w")
        # self.button_set_actuator_position = ttk.Button(
        #     frame_1_2, text="Set Position", command=self.on_set_actuator_position)
        # self.button_set_actuator_position.pack(side="top", anchor="w")
        # self.button_home_actuator = ttk.Button(
        #     frame_1_2, text="Home", command=self.on_home_actuator)
        # self.button_home_actuator.pack(side="top", anchor="w")
        # ttk.Label(frame_1_3, text="Current NDFilter Angle (deg): ").pack(
        #     side="top", anchor="w")
        # ttk.Entry(frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_angle).pack(
        #     side="top", anchor="w")
        # ttk.Label(frame_1_3, text="Target Angle (deg): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_target_angle = Spinbox(frame_1_3, from_=0, to=360, increment=0.1,
        #                                     textvariable=VARIABLES.var_spinbox_target_angle)
        # self.spinbox_target_angle.pack(side="top", anchor="w")
        # self.button_set_angle = ttk.Button(
        #     frame_1_3, text="Set Angle", command=self.on_set_angle)
        # self.button_set_angle.pack(side="top", anchor="w")
        # ttk.Label(frame_1_4, text="Sweep Start Wavelength (nm): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_sweep_start_wavelength = Spinbox(frame_1_4, from_=0, to=float(
        #     "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_start_wavelength)
        # self.spinbox_sweep_start_wavelength.pack(side="top", anchor="w")
        # ttk.Label(frame_1_4, text="Sweep End Wavelength (nm): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_sweep_end_wavelength = Spinbox(frame_1_4, from_=0, to=float(
        #     "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_end_wavelength)
        # self.spinbox_sweep_end_wavelength.pack(side="top", anchor="w")
        # ttk.Label(frame_1_4, text="Sweep Step Size (nm): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_sweep_step_size = Spinbox(frame_1_4, from_=0, to=float(
        #     "inf"), textvariable=VARIABLES.var_spinbox_sweep_step_size)
        # ttk.Label(frame_1_5, text="Current Power (rel. uW): ").pack(
        #     side="top", anchor="w")
        # ttk.Entry(frame_1_5, state="readonly", textvariable=VARIABLES.var_entry_curr_power).pack(
        #     side="top", anchor="w")
        # self.button_power = ttk.Button(
        #     frame_1_5, text="Turn ON", command=self.toggle_power_reading)
        # self.button_power.pack(side="top", anchor="w")
        # self.button_set_background_power = ttk.Button(
        #     frame_1_5, text="Set As Background Power", command=UTILS.set_background_power)
        # self.button_set_background_power.pack(side="top", anchor="w")
        # ttk.Label(frame_1_5, text="Background Power (uW):").pack(
        #     side="top", anchor="w")
        # self.spinbox_background_power = Spinbox(frame_1_5, from_=0, to=float(
        #     "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        # self.spinbox_background_power.pack(side="top", anchor="w")
        # ttk.Label(frame_1_5, text="Target Power (uW): ").pack(
        #     side="top", anchor="w")
        # self.spinbox_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
        #                                     textvariable=VARIABLES.var_spinbox_sweep_target_power)
        # self.spinbox_target_power.pack(side="top", anchor="w")
        # VARIABLES.var_spinbox_sweep_target_power.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        # ttk.Label(frame_1_5, text="Wavelength at target power (nm)\n(for fixed photon flux mode)").pack(side="top", anchor="w")
        # self.spinbox_wavelength_at_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
        #         textvariable=VARIABLES.var_spinbox_wavelength_at_target_power)
        # self.spinbox_wavelength_at_target_power.pack(side="top", anchor="w")
        # VARIABLES.var_spinbox_wavelength_at_target_power.trace_add("write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        # self.label_oscilloscope_wait_time = ttk.Label(
        #     frame_1_6, text="Oscilloscope wait time (s): ")
        # self.label_oscilloscope_wait_time.pack(side="top", anchor="w")
        # self.spinbox_sweep_oscilloscope_wait_time = Spinbox(frame_1_6, from_=0, to=float(
        #     "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_wait_time)
        # self.spinbox_sweep_oscilloscope_wait_time.pack(side="top", anchor="w")
        # ttk.Label(frame_1_6, text="Number of measurements\nper wavelength").pack(
        #     side="top", anchor="w")
        # self.spinbox_sweep_lifetime_num = Spinbox(frame_1_6, from_=0, to=float(
        #     "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_num)
        # self.spinbox_sweep_lifetime_num.pack(side="top", anchor="w")
        # ttk.Label(frame_1_6, text="Actuator explore range\nfor max power (∓mm, Δ)").pack(
        #     side="top", anchor="w")
        # self.spinbox_sweep_actuator_explore_range_negative = Spinbox(frame_1_6, from_=-float("inf"), to=0, increment=0.01, width=5,
        #                                                              textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_negative)
        # self.spinbox_sweep_actuator_explore_range_negative.pack(side="left")
        # self.spinbox_sweep_actuator_explore_range_positive = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
        #                                                              textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_positive)
        # self.spinbox_sweep_actuator_explore_range_positive.pack(side="left")
        # self.spinbox_sweep_actuator_explore_range_step_size = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
        #                                                               textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_step_size)
        # self.spinbox_sweep_actuator_explore_range_step_size.pack(side="left")
        # ttk.Label(frame_2_1, text="Ch1 Instant (V-s)").pack(side="top")
        # self.plot_lifetime_instant_ch1 = Plot(frame_2_1)
        # ttk.Label(frame_2_2, text="Ch1 Average (V-s)").pack(side="top")
        # self.plot_lifetime_average_ch1 = Plot(frame_2_2)
        # ttk.Label(frame_3_1, text="Ch2 Instant (V-s)").pack(side="top")
        # self.plot_lifetime_instant_ch2 = Plot(frame_3_1)
        # ttk.Label(frame_3_2, text="Ch2 Average (V-s)").pack(side="top")
        # self.plot_lifetime_average_ch2 = Plot(frame_3_2)
        return frame