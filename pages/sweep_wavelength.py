from tkinter import ttk
from tkinter.filedialog import askopenfilename
from utils.config import INSTANCES, VARIABLES, LOGGER, UTILS
from utils.spinbox import Spinbox
from utils.plot import Plot
from utils.task import Task, RUNNING, PAUSED, PAUSING, TERMINATING
from utils.save import Save
from pages.sweep_wavelength_modules.read_power import ReadPowerTask
from pages.sweep_wavelength_modules.set_angle import SetAngleTask
from pages.sweep_wavelength_modules.set_wavelength import SetWavelengthTask
from pages.sweep_wavelength_modules.set_actuator_position import SetActuatorPositionTask
from pages.sweep_wavelength_modules.home_actuator import HomeActuatorTask
from pages.sweep_wavelength_modules.home_ndfilter import HomeNDFilterTask
from pages.sweep_wavelength_modules.sweep_wavelength import SweepWavelengthTask
from pages.sweep_wavelength_modules.calibrate_actuator import CalibrateActuatorTask
from pages.sweep_wavelength_modules.sweep_wavelength_boxcar_heatmap import SweepWavelengthBoxcarHeatmapTask
from pages.sweep_wavelength_modules.calibrate_ndfilter import CalibrateNDFilterTask
from pages.sweep_wavelength_modules.sweep_wavelength_boxcar_single_power import SweepWavelengthBoxcarSinglePowerTask
from pages.sweep_wavelength_modules.sweep_wavelength_lockin_single_power import SweepWavelengthLockinSinglePowerTask
from pages.sweep_wavelength_modules.sweep_wavelength_lockin_heatmap import SweepWavelengthLockinHeatmapTask


class SweepWavelength:
    def __init__(self, parent) -> None:
        self.frame, frame_oscilloscope_3, frame_calibrate_actuator_2, frame_boxcar_heapmap_3, \
            frame_calibrate_ndfilter_3, frame_boxcar_single_power_3, frame_lockin_single_power_3, \
            frame_lockin_heatmap_4 \
            = self.set_frame(parent)
        self.set_angle_task = SetAngleTask(self.button_set_angle)
        self.read_power_task = ReadPowerTask(self.button_power)
        self.set_wavelength_task = SetWavelengthTask(
            self.button_set_wavelength)
        self.set_actuator_position_task = SetActuatorPositionTask(
            self.button_set_actuator_position)
        self.home_actuator_task = HomeActuatorTask(self.button_home_actuator)
        self.home_ndfilter_task = HomeNDFilterTask(self.button_home_ndfilter)
        self.save_oscilloscope = Save(frame_oscilloscope_3, VARIABLES.var_entry_sweep_wavelength_directory,
                                      VARIABLES.var_entry_sweep_wavelength_filename,
                                      substitute_dict={})
        self.save_calibrate_actuator = Save(frame_calibrate_actuator_2, VARIABLES.var_entry_calibrate_actuator_directory,
                                            VARIABLES.var_entry_calibrate_actuator_filename,
                                            substitute_dict={})
        self.save_boxcar_heatmap = Save(frame_boxcar_heapmap_3, VARIABLES.var_entry_sweep_wavelength_boxcar_heatmap_directory,
                                        VARIABLES.var_entry_sweep_wavelength_boxcar_heatmap_filename,
                                        substitute_dict={})
        self.save_calibrate_ndfilter = Save(frame_calibrate_ndfilter_3, VARIABLES.var_entry_calibrate_ndfilter_directory,
                                            VARIABLES.var_entry_calibrate_ndfilter_filename,
                                            substitute_dict={})
        self.save_boxcar_single_power = Save(frame_boxcar_single_power_3, VARIABLES.var_entry_sweep_wavelength_boxcar_single_power_directory,
                                             VARIABLES.var_entry_sweep_wavelength_boxcar_single_power_filename,
                                             substitute_dict={'power': VARIABLES.var_spinbox_sweep_target_power.get()})
        self.save_lockin_single_power = Save(frame_lockin_single_power_3, VARIABLES.var_entry_sweep_wavelength_lockin_single_power_directory,
                                             VARIABLES.var_entry_sweep_wavelength_lockin_single_power_filename,
                                             substitute_dict={'power': VARIABLES.var_spinbox_sweep_target_power.get()})
        self.save_lockin_heatmap = Save(frame_lockin_heatmap_4, VARIABLES.var_entry_sweep_wavelength_lockin_heatmap_directory,
                                        VARIABLES.var_entry_sweep_wavelength_lockin_heatmap_filename,
                                        substitute_dict={})
        SweepWavelengthTask(frame_oscilloscope_3, self)
        CalibrateActuatorTask(frame_calibrate_actuator_2, self)
        SweepWavelengthBoxcarHeatmapTask(frame_boxcar_heapmap_3, self)
        CalibrateNDFilterTask(frame_calibrate_ndfilter_3, self)
        SweepWavelengthBoxcarSinglePowerTask(frame_boxcar_single_power_3, self)
        SweepWavelengthLockinSinglePowerTask(frame_lockin_single_power_3, self)
        SweepWavelengthLockinHeatmapTask(frame_lockin_heatmap_4, self)
        self.on_change_for_photon_flux_fixed()

    def set_frame(self, parent):
        frame = ttk.Frame(parent)
        frame_1 = ttk.Frame(frame)
        frame_1.pack(side="top", anchor="w", padx=10, pady=10)
        frame_tab = ttk.Frame(frame)
        frame_tab.pack(side="top", anchor="w", padx=10, pady=10)
        tabControl = ttk.Notebook(frame_tab)
        frame_oscilloscope = ttk.Frame(tabControl)
        frame_oscilloscope.pack(side="top", anchor="w", padx=10, pady=10)
        frame_calibrate_actuator = ttk.Frame(tabControl)
        frame_calibrate_actuator.pack(side="top", anchor="w", padx=10, pady=10)
        frame_boxcar_heapmap = ttk.Frame(tabControl)
        frame_boxcar_heapmap.pack(side="top", anchor="w", padx=10, pady=10)
        frame_calibrate_ndfilter = ttk.Frame(tabControl)
        frame_calibrate_ndfilter.pack(side="top", anchor="w", padx=10, pady=10)
        frame_boxcar_single_power = ttk.Frame(tabControl)
        frame_boxcar_single_power.pack(
            side="top", anchor="w", padx=10, pady=10)
        frame_lockin_single_power = ttk.Frame(tabControl)
        frame_lockin_single_power.pack(
            side="top", anchor="w", padx=10, pady=10)
        frame_lockin_heatmap = ttk.Frame(tabControl)
        frame_lockin_heatmap.pack(side="top", anchor="w", padx=10, pady=10)
        tabControl.add(frame_oscilloscope, text="Oscilloscope")
        tabControl.add(frame_calibrate_actuator, text="Calibrate Actuator")
        tabControl.add(frame_calibrate_ndfilter, text="Calibrate NDFilter")
        tabControl.add(frame_boxcar_heapmap, text="Boxcar (Heatmap)")
        tabControl.add(frame_boxcar_single_power, text="Boxcar (Single Power)")
        tabControl.add(frame_lockin_single_power,
                       text="Lockin (FIANIUM Single Power)")
        tabControl.add(frame_lockin_heatmap, text="Lockin (FIANIUM Heatmap)")
        tabControl.pack(side="top", fill="both", expand=True)
        frame_oscilloscope_1 = ttk.Frame(frame_oscilloscope)
        frame_oscilloscope_1.pack(side="top", padx=10)
        frame_oscilloscope_2 = ttk.Frame(frame_oscilloscope)
        frame_oscilloscope_2.pack(side="top", padx=10, pady=10)
        frame_oscilloscope_3 = ttk.Frame(frame_oscilloscope)
        frame_oscilloscope_3.pack(side="top", anchor="n", padx=10)
        frame_calibrate_actuator_1 = ttk.Frame(frame_calibrate_actuator)
        frame_calibrate_actuator_1.pack(side="top", anchor="n", padx=10)
        frame_calibrate_actuator_2 = ttk.Frame(frame_calibrate_actuator)
        frame_calibrate_actuator_2.pack(side="top", anchor="n", padx=10)
        frame_boxcar_heapmap_1 = ttk.Frame(frame_boxcar_heapmap)
        frame_boxcar_heapmap_1.pack(side="top", anchor="n", padx=10)
        frame_boxcar_heapmap_2 = ttk.Frame(frame_boxcar_heapmap)
        frame_boxcar_heapmap_2.pack(side="top", anchor="n", padx=10)
        frame_boxcar_heapmap_3 = ttk.Frame(frame_boxcar_heapmap)
        frame_boxcar_heapmap_3.pack(side="top", anchor="n", padx=10)
        frame_calibrate_ndfilter_1 = ttk.Frame(frame_calibrate_ndfilter)
        frame_calibrate_ndfilter_1.pack(side="top", anchor="n", padx=10)
        frame_calibrate_ndfilter_2 = ttk.Frame(frame_calibrate_ndfilter)
        frame_calibrate_ndfilter_2.pack(side="top", anchor="n", padx=10)
        frame_calibrate_ndfilter_3 = ttk.Frame(frame_calibrate_ndfilter)
        frame_calibrate_ndfilter_3.pack(side="top", anchor="n", padx=10)
        frame_boxcar_single_power_1 = ttk.Frame(frame_boxcar_single_power)
        frame_boxcar_single_power_1.pack(side="top", anchor="n", padx=10)
        frame_boxcar_single_power_2 = ttk.Frame(frame_boxcar_single_power)
        frame_boxcar_single_power_2.pack(side="top", anchor="n", padx=10)
        frame_boxcar_single_power_3 = ttk.Frame(frame_boxcar_single_power)
        frame_boxcar_single_power_3.pack(side="top", anchor="n", padx=10)
        frame_lockin_single_power_1 = ttk.Frame(frame_lockin_single_power)
        frame_lockin_single_power_1.pack(side="top", anchor="n", padx=10)
        frame_lockin_single_power_2 = ttk.Frame(frame_lockin_single_power)
        frame_lockin_single_power_2.pack(side="top", anchor="n", padx=10)
        frame_lockin_single_power_3 = ttk.Frame(frame_lockin_single_power)
        frame_lockin_single_power_3.pack(side="top", anchor="n", padx=10)
        frame_lockin_heatmap_1 = ttk.Frame(frame_lockin_heatmap)
        frame_lockin_heatmap_1.pack(side="top", anchor="n", padx=10)
        frame_lockin_heatmap_2 = ttk.Frame(frame_lockin_heatmap)
        frame_lockin_heatmap_2.pack(side="top", anchor="n", padx=10)
        frame_lockin_heatmap_3 = ttk.Frame(frame_lockin_heatmap)
        frame_lockin_heatmap_3.pack(side="top", anchor="n", padx=10)
        frame_lockin_heatmap_4 = ttk.Frame(frame_lockin_heatmap)
        frame_lockin_heatmap_4.pack(side="top", anchor="n", padx=10)
        frame_1_1 = ttk.Frame(frame_1)
        frame_1_1.pack(side="left", anchor="n", padx=10)
        frame_1_2 = ttk.Frame(frame_1)
        frame_1_2.pack(side="left", anchor="n", padx=10)
        frame_1_3 = ttk.Frame(frame_1)
        frame_1_3.pack(side="left", anchor="n", padx=10)
        frame_1_4 = ttk.Frame(frame_1)
        frame_1_4.pack(side="left", anchor="n", padx=10)
        frame_1_5 = ttk.Frame(frame_1)
        frame_1_5.pack(side="left", anchor="n", padx=10)
        frame_1_6 = ttk.Frame(frame_1)
        frame_1_6.pack(side="left", anchor="n", padx=10)
        frame_oscilloscope_1_1 = ttk.Frame(frame_oscilloscope_1)
        frame_oscilloscope_1_1.pack(side="left", anchor="n", padx=10)
        frame_oscilloscope_1_2 = ttk.Frame(frame_oscilloscope_1)
        frame_oscilloscope_1_2.pack(side="left", anchor="n", padx=10)
        frame_oscilloscope_2_1 = ttk.Frame(frame_oscilloscope_2)
        frame_oscilloscope_2_1.pack(side="left", anchor="n", padx=10)
        frame_oscilloscope_2_2 = ttk.Frame(frame_oscilloscope_2)
        frame_oscilloscope_2_2.pack(side="left", anchor="n", padx=10)
        frame_boxcar_heapmap_2_1 = ttk.Frame(frame_boxcar_heapmap_2)
        frame_boxcar_heapmap_2_1.pack(side="left", anchor="n", padx=10)
        frame_boxcar_heapmap_2_2 = ttk.Frame(frame_boxcar_heapmap_2)
        frame_boxcar_heapmap_2_2.pack(side="left", anchor="n", padx=10)
        frame_calibrate_ndfilter_2_1 = ttk.Frame(frame_calibrate_ndfilter_2)
        frame_calibrate_ndfilter_2_1.pack(side="left", anchor="n", padx=10)
        frame_calibrate_ndfilter_2_2 = ttk.Frame(frame_calibrate_ndfilter_2)
        frame_calibrate_ndfilter_2_2.pack(side="left", anchor="n", padx=10)
        frame_lockin_single_power_2_1 = ttk.Frame(frame_lockin_single_power_2)
        frame_lockin_single_power_2_1.pack(side="left", anchor="n", padx=10)
        frame_lockin_single_power_2_2 = ttk.Frame(frame_lockin_single_power_2)
        frame_lockin_single_power_2_2.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_2_1 = ttk.Frame(frame_lockin_heatmap_2)
        frame_lockin_heatmap_2_1.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_2_2 = ttk.Frame(frame_lockin_heatmap_2)
        frame_lockin_heatmap_2_2.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_2_3 = ttk.Frame(frame_lockin_heatmap_2)
        frame_lockin_heatmap_2_3.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_2_4 = ttk.Frame(frame_lockin_heatmap_2)
        frame_lockin_heatmap_2_4.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_3_1 = ttk.Frame(frame_lockin_heatmap_3)
        frame_lockin_heatmap_3_1.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_3_2 = ttk.Frame(frame_lockin_heatmap_3)
        frame_lockin_heatmap_3_2.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_3_3 = ttk.Frame(frame_lockin_heatmap_3)
        frame_lockin_heatmap_3_3.pack(side="left", anchor="n", padx=10)
        frame_lockin_heatmap_3_4 = ttk.Frame(frame_lockin_heatmap_3)
        frame_lockin_heatmap_3_4.pack(side="left", anchor="n", padx=10)
        ttk.Label(frame_1_1, text="Current Wavelength (nm):").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_1, state="readonly", textvariable=VARIABLES.var_entry_curr_wavelength).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_1, text="Target Wavelength (nm):").pack(
            side="top", anchor="w")
        self.spinbox_target_wavelength = Spinbox(frame_1_1, from_=0, to=float("inf"),
                                                 textvariable=VARIABLES.var_spinbox_target_wavelength)
        self.spinbox_target_wavelength.pack(side="top", anchor="w")
        self.button_set_wavelength = ttk.Button(
            frame_1_1, text="Set Wavelength", command=self.on_set_wavelength)
        self.button_set_wavelength.pack(side="top", anchor="w")
        ttk.Label(frame_1_2, text="Actuator Position (mm): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_2, state="readonly", textvariable=VARIABLES.var_entry_curr_actuator_position).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_2, text="Target Actuator Position (mm): ").pack(
            side="top", anchor="w")
        self.spinbox_target_actuator_position = Spinbox(frame_1_2, from_=0, to=float("inf"), increment=0.01,
                                                        textvariable=VARIABLES.var_spinbox_target_actuator_position)
        self.spinbox_target_actuator_position.pack(side="top", anchor="w")
        self.button_set_actuator_position = ttk.Button(
            frame_1_2, text="Set Position", command=self.on_set_actuator_position)
        self.button_set_actuator_position.pack(side="top", anchor="w")
        self.button_home_actuator = ttk.Button(
            frame_1_2, text="Home", command=self.on_home_actuator)
        self.button_home_actuator.pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Current NDFilter Angle (deg): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_3, state="readonly", textvariable=VARIABLES.var_entry_curr_angle).pack(
            side="top", anchor="w")
        ttk.Label(frame_1_3, text="Target Angle (deg): ").pack(
            side="top", anchor="w")
        self.spinbox_target_angle = Spinbox(frame_1_3, from_=0, to=360, increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_target_angle)
        self.spinbox_target_angle.pack(side="top", anchor="w")
        self.button_set_angle = ttk.Button(
            frame_1_3, text="Set Angle", command=self.on_set_angle)
        self.button_set_angle.pack(side="top", anchor="w")
        self.button_home_ndfilter = ttk.Button(
            frame_1_3, text="Home", command=self.on_home_ndfilter)
        self.button_home_ndfilter.pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="Note: Make sure power decreases\nwith NDFilter angle.",
                  font="TkDefaultFont 8").pack(side="top", anchor="w")
        ttk.Label(frame_1_3, text="NDFilter Spin Relative Speed (default 1.0)").pack(
            side="top", anchor="w")
        Spinbox(frame_1_3, from_=0, to=float("inf"), increment=1,
                textvariable=VARIABLES.var_spinbox_ndfilter_speed).pack(side="top", anchor="w")
        ttk.Label(frame_1_4, text="Sweep Start Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_start_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_start_wavelength)
        self.spinbox_sweep_start_wavelength.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_start_wavelength.trace_add(
            "write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_4, text="Sweep End Wavelength (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_end_wavelength = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_sweep_end_wavelength)
        self.spinbox_sweep_end_wavelength.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_end_wavelength.trace_add(
            "write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_4, text="Sweep Step Size (nm): ").pack(
            side="top", anchor="w")
        self.spinbox_sweep_step_size = Spinbox(frame_1_4, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_step_size)
        self.spinbox_sweep_step_size.pack(side="top", anchor="w")
        self.checkbutton_photon_flux_fixed = ttk.Checkbutton(
            frame_1_4, text="Photon Flux Fixed\n(instead of power fixed)", variable=VARIABLES.var_checkbutton_photon_flux_fixed)
        self.checkbutton_photon_flux_fixed.pack(side="top", anchor="w")
        VARIABLES.var_checkbutton_photon_flux_fixed.trace_add(
            "write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        self.label_photon_flux_fixed = ttk.Label(frame_1_4, text="\n\n")
        self.label_photon_flux_fixed.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Current Power (rel. uW): ").pack(
            side="top", anchor="w")
        ttk.Entry(frame_1_5, state="readonly", textvariable=VARIABLES.var_entry_curr_power).pack(
            side="top", anchor="w")
        self.button_power = ttk.Button(
            frame_1_5, text="Turn ON", command=self.toggle_power_reading)
        self.button_power.pack(side="top", anchor="w")
        self.button_set_background_power = ttk.Button(
            frame_1_5, text="Set As Background Power", command=UTILS.set_background_power)
        self.button_set_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Background Power (uW):").pack(
            side="top", anchor="w")
        self.spinbox_background_power = Spinbox(frame_1_5, from_=0, to=float(
            "inf"), increment=0.1, textvariable=VARIABLES.var_spinbox_background_power)
        self.spinbox_background_power.pack(side="top", anchor="w")
        ttk.Label(frame_1_5, text="Target Power (uW): ").pack(
            side="top", anchor="w")
        self.spinbox_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
                                            textvariable=VARIABLES.var_spinbox_sweep_target_power)
        self.spinbox_target_power.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_sweep_target_power.trace_add(
            "write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        ttk.Label(frame_1_5, text="Wavelength at target power (nm)\n(for fixed photon flux mode)").pack(
            side="top", anchor="w")
        self.spinbox_wavelength_at_target_power = Spinbox(frame_1_5, from_=0, to=float("inf"), increment=0.1,
                                                          textvariable=VARIABLES.var_spinbox_wavelength_at_target_power)
        self.spinbox_wavelength_at_target_power.pack(side="top", anchor="w")
        VARIABLES.var_spinbox_wavelength_at_target_power.trace_add(
            "write", lambda val, index, mode: self.on_change_for_photon_flux_fixed())
        self.label_oscilloscope_wait_time = ttk.Label(
            frame_1_6, text="Oscilloscope wait time (s): ")
        self.label_oscilloscope_wait_time.pack(side="top", anchor="w")
        self.spinbox_sweep_oscilloscope_wait_time = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_wait_time)
        self.spinbox_sweep_oscilloscope_wait_time.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Number of measurements\nper wavelength").pack(
            side="top", anchor="w")
        self.spinbox_sweep_lifetime_num = Spinbox(frame_1_6, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_sweep_lifetime_num)
        self.spinbox_sweep_lifetime_num.pack(side="top", anchor="w")
        ttk.Label(frame_1_6, text="Actuator explore range\nfor max power (∓mm, Δ)").pack(
            side="top", anchor="w")
        self.spinbox_sweep_actuator_explore_range_negative = Spinbox(frame_1_6, from_=-float("inf"), to=0, increment=0.01, width=5,
                                                                     textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_negative)
        self.spinbox_sweep_actuator_explore_range_negative.pack(side="left")
        self.spinbox_sweep_actuator_explore_range_positive = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
                                                                     textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_positive)
        self.spinbox_sweep_actuator_explore_range_positive.pack(side="left")
        self.spinbox_sweep_actuator_explore_range_step_size = Spinbox(frame_1_6, from_=0, to=float("inf"), increment=0.01, width=5,
                                                                      textvariable=VARIABLES.var_spinbox_sweep_actuator_explore_range_step_size)
        self.spinbox_sweep_actuator_explore_range_step_size.pack(side="left")
        ttk.Label(frame_oscilloscope_1_1,
                  text="Ch1 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch1 = Plot(frame_oscilloscope_1_1)
        ttk.Label(frame_oscilloscope_1_2,
                  text="Ch1 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch1 = Plot(frame_oscilloscope_1_2)
        ttk.Label(frame_oscilloscope_2_1,
                  text="Ch2 Instant (V-s)").pack(side="top")
        self.plot_lifetime_instant_ch2 = Plot(frame_oscilloscope_2_1)
        ttk.Label(frame_oscilloscope_2_2,
                  text="Ch2 Average (V-s)").pack(side="top")
        self.plot_lifetime_average_ch2 = Plot(frame_oscilloscope_2_2)
        ttk.Label(frame_calibrate_actuator_1,
                  text="Please first manually set actuator position at the max power for starting wavelength.").pack(side="top")
        ttk.Label(frame_calibrate_actuator_1,
                  text="Optimal Actuator Position (mm-nm)").pack(side="top")
        self.plot_calibrate_actuator = Plot(
            frame_calibrate_actuator_1, figsize=(13, 5))
        ttk.Label(frame_boxcar_heapmap_1, text="Path to actuator calibration file").pack(
            side="left")
        ttk.Entry(frame_boxcar_heapmap_1, textvariable=VARIABLES.var_entry_actuator_calibration_file,
                  width=60).pack(side="left")
        ttk.Label(frame_boxcar_heapmap_2_1,
                  text="Boxcar Curve (V-uW)").pack(side="top")
        self.plot_boxcar_curve = Plot(frame_boxcar_heapmap_2_1)
        ttk.Label(frame_boxcar_heapmap_2_2,
                  text="Boxcar Heatmap (uW-nm z:V)").pack(side="top")
        self.plot_boxcar_heatmap = Plot(frame_boxcar_heapmap_2_2)
        ttk.Button(frame_boxcar_heapmap_1, text="Browse",
                   command=self.browse_actuator_calibration_file).pack(side="left")
        ttk.Label(frame_boxcar_heapmap_3,
                  text="Ending Angle (deg)").pack(side="top")
        Spinbox(frame_boxcar_heapmap_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_entry_heatmap_ending_angle).pack(side="top", pady=(0, 10))
        ttk.Label(frame_calibrate_ndfilter_1, text="Path to actuator calibration file").pack(
            side="left")
        ttk.Entry(frame_calibrate_ndfilter_1, textvariable=VARIABLES.var_entry_actuator_calibration_file,
                  width=60).pack(side="left")
        ttk.Button(frame_calibrate_ndfilter_1, text="Browse",
                   command=self.browse_actuator_calibration_file).pack(side="left")
        ttk.Label(frame_calibrate_ndfilter_2_1,
                  text="Power vs NDfilter (uW-degree)").pack(side="top")
        self.plot_calibrate_ndfilter_curve = Plot(frame_calibrate_ndfilter_2_1)
        ttk.Label(frame_calibrate_ndfilter_2_2,
                  text="Power vs NDfilter Heatmap (degree-nm z:uW)").pack(side="top")
        self.plot_calibrate_ndfilter_heatmap = Plot(
            frame_calibrate_ndfilter_2_2)
        ttk.Label(frame_calibrate_ndfilter_3,
                  text="Starting Angle with max power (deg)").pack(side="top")
        self.spinbox_calibrate_ndfilter_starting_angle = Spinbox(frame_calibrate_ndfilter_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_calibrate_ndfilter_starting_angle)
        self.spinbox_calibrate_ndfilter_starting_angle.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_calibrate_ndfilter_3,
                  text="Ending Angle (deg)").pack(side="top")
        self.spinbox_calibrate_ndfilter_ending_angle = Spinbox(frame_calibrate_ndfilter_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_calibrate_ndfilter_ending_angle)
        self.spinbox_calibrate_ndfilter_ending_angle.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_calibrate_ndfilter_3,
                  text="Steps (steps will be taken in exp scale, default 100)").pack(side="top")
        self.spinbox_calibrate_actuator_steps = Spinbox(frame_calibrate_ndfilter_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_calibrate_ndfilter_steps)
        self.spinbox_calibrate_actuator_steps.pack(side="top", pady=(0, 10))
        ttk.Label(frame_boxcar_single_power_1, text="Path to actuator calibration file").pack(
            side="left")
        ttk.Entry(frame_boxcar_single_power_1, textvariable=VARIABLES.var_entry_actuator_calibration_file,
                  width=60).pack(side="left")
        ttk.Button(frame_boxcar_single_power_1, text="Browse",
                   command=self.browse_actuator_calibration_file).pack(side="left")
        self.plot_boxcar_single_power = Plot(frame_boxcar_single_power_2)
        ttk.Label(frame_boxcar_single_power_3,
                  text="Remember to set \"Target Power (uW)\" above").pack(side="top")
        ttk.Label(frame_boxcar_single_power_3,
                  text="NDFilter offset angle (for accurate angle prediction from power)").pack(side="top")
        self.spinbox_boxcar_single_power_ndfilter_offset_angle = Spinbox(frame_boxcar_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_single_power_ndfilter_offset_angle)
        self.spinbox_boxcar_single_power_ndfilter_offset_angle.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_boxcar_single_power_3,
                  text="Time interval between Boxcar data acquisitions (s) (should be larger than sliding window averaging time)").pack(side="top")
        self.spinbox_boxcar_single_power_time_interval = Spinbox(frame_boxcar_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_boxcar_single_power_time_interval)
        self.spinbox_boxcar_single_power_time_interval.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_boxcar_single_power_3,
                  text="Number of data acquisitions").pack(side="top")
        self.spinbox_boxcar_single_power_number_of_data_acquisitions = Spinbox(frame_boxcar_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_boxcar_single_power_number_of_data_acquisitions)
        self.spinbox_boxcar_single_power_number_of_data_acquisitions.pack(
            side="top", pady=(0, 10))
        ttk.Label(frame_lockin_single_power_1, text="Path to actuator calibration file").pack(
            side="left")
        ttk.Entry(frame_lockin_single_power_1, textvariable=VARIABLES.var_entry_actuator_calibration_file,
                  width=60).pack(side="left")
        ttk.Button(frame_lockin_single_power_1, text="Browse",
                   command=self.browse_actuator_calibration_file).pack(side="left")
        ttk.Label(frame_lockin_single_power_2_1,
                    text="Ch1 (V-nm)").pack(side="top")
        self.plot_lockin_single_power_ch1 = Plot(frame_lockin_single_power_2_1)
        ttk.Label(frame_lockin_single_power_2_2,
                    text="Ch2 (V-nm)").pack(side="top")
        self.plot_lockin_single_power_ch2 = Plot(frame_lockin_single_power_2_2)
        ttk.Label(frame_lockin_single_power_3,
                  text="Remember to set \"Target Power (uW)\" above").pack(side="top")
        ttk.Label(frame_lockin_single_power_3,
                  text="NDFilter offset angle (for accurate angle prediction from power)").pack(side="top")
        self.spinbox_lockin_single_power_ndfilter_offset_angle = Spinbox(frame_lockin_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_single_power_ndfilter_offset_angle)
        self.spinbox_lockin_single_power_ndfilter_offset_angle.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_lockin_single_power_3,
                  text="Time interval between Lockin data acquisitions (s) (should be larger than sliding window averaging time)").pack(side="top")
        self.spinbox_lockin_single_power_time_interval = Spinbox(frame_lockin_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_lockin_single_power_time_interval)
        self.spinbox_lockin_single_power_time_interval.pack(
            side="top", pady=(0, 0))
        ttk.Label(frame_lockin_single_power_3,
                  text="Number of data acquisitions").pack(side="top")
        self.spinbox_lockin_single_power_number_of_data_acquisitions = Spinbox(frame_lockin_single_power_3, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_spinbox_lockin_single_power_number_of_data_acquisitions)
        self.spinbox_lockin_single_power_number_of_data_acquisitions.pack(
            side="top", pady=(0, 10))
        ttk.Label(frame_lockin_heatmap_1, text="Path to actuator calibration file").pack(
            side="left")
        ttk.Entry(frame_lockin_heatmap_1, textvariable=VARIABLES.var_entry_actuator_calibration_file,
                    width=60).pack(side="left")
        ttk.Button(frame_lockin_heatmap_1, text="Browse",
                    command=self.browse_actuator_calibration_file).pack(side="left")
        ttk.Label(frame_lockin_heatmap_2_1,
                    text="Current Ch1 Trace (V-uW)").pack(side="top")
        self.plot_lockin_curve_ch1_trace = Plot(frame_lockin_heatmap_2_1, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_2_2,
                    text="Current Ch1 Retrace (V-uW)").pack(side="top")
        self.plot_lockin_curve_ch1_retrace = Plot(frame_lockin_heatmap_2_2, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_2_3,
                    text="Current Ch2 Trace (V-uW)").pack(side="top")
        self.plot_lockin_curve_ch2_trace = Plot(frame_lockin_heatmap_2_3, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_2_4,
                    text="Current Ch2 Retrace (V-uW)").pack(side="top")
        self.plot_lockin_curve_ch2_retrace = Plot(frame_lockin_heatmap_2_4, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_3_1,
                    text="Ch1 Heatmap Trace (uW-nm z:V)").pack(side="top")
        self.plot_lockin_heatmap_ch1_trace = Plot(frame_lockin_heatmap_3_1, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_3_2,
                    text="Ch1 Heatmap Retrace (uW-nm z:V)").pack(side="top")
        self.plot_lockin_heatmap_ch1_retrace = Plot(frame_lockin_heatmap_3_2, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_3_3,
                    text="Ch2 Heatmap Trace (uW-nm z:V)").pack(side="top")
        self.plot_lockin_heatmap_ch2_trace = Plot(frame_lockin_heatmap_3_3, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_3_4,
                    text="Ch2 Heatmap Retrace (uW-nm z:V)").pack(side="top")
        self.plot_lockin_heatmap_ch2_retrace = Plot(frame_lockin_heatmap_3_4, figsize=(6, 2))
        ttk.Label(frame_lockin_heatmap_4,
                    text="Starting Angle (deg)").pack(side="top")
        Spinbox(frame_lockin_heatmap_4, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_entry_heatmap_starting_angle).pack(side="top", pady=(0, 0))
        ttk.Label(frame_lockin_heatmap_4,
                    text="Ending Angle (deg)").pack(side="top")
        Spinbox(frame_lockin_heatmap_4, from_=0, to=float(
            "inf"), textvariable=VARIABLES.var_entry_heatmap_ending_angle).pack(side="top", pady=(0, 10))
        return frame, frame_oscilloscope_3, frame_calibrate_actuator_2, frame_boxcar_heapmap_3,\
            frame_calibrate_ndfilter_3, frame_boxcar_single_power_3, frame_lockin_single_power_3, \
            frame_lockin_heatmap_4

    def toggle_power_reading(self):
        if self.read_power_task.is_running:
            self.turn_off_power_reading()
        else:
            self.turn_on_power_reading()

    def on_change_for_photon_flux_fixed(self):
        if VARIABLES.var_checkbutton_photon_flux_fixed.get():
            self.spinbox_wavelength_at_target_power.config(state="normal")
            target_wavelength = float(
                VARIABLES.var_spinbox_wavelength_at_target_power.get())
            start_wavelength = float(
                VARIABLES.var_spinbox_sweep_start_wavelength.get())
            end_wavelength = float(
                VARIABLES.var_spinbox_sweep_end_wavelength.get())
            target_power = round(
                float(VARIABLES.var_spinbox_sweep_target_power.get()), 6)
            start_power = round(
                target_power * target_wavelength / start_wavelength, 6)
            end_power = round(
                target_power * target_wavelength / end_wavelength, 6)
            pair_to_display = []
            pair_to_display.append((start_wavelength, start_power))
            if (target_wavelength, target_power) not in pair_to_display:
                pair_to_display.append((target_wavelength, target_power))
            if (end_wavelength, end_power) not in pair_to_display:
                pair_to_display.append((end_wavelength, end_power))
            pair_to_display.sort(key=lambda x: x[0])
            text_to_display = ""
            for pair in pair_to_display:
                text_to_display += str(pair[0]) + \
                    "nm: " + str(pair[1]) + "uW\n"
            if len(pair_to_display) == 1:
                text_to_display += "\n\n"
            elif len(pair_to_display) == 2:
                text_to_display += "\n"
            self.label_photon_flux_fixed.config(text=text_to_display[:-1])
        else:
            self.spinbox_wavelength_at_target_power.config(state="disabled")
            self.label_photon_flux_fixed.config(text="\n\n")

    def turn_off_power_reading(self):
        self.button_power.config(state="disabled")
        self.read_power_task.terminate()
        self.button_power["text"] = "Turn ON"

    def turn_on_power_reading(self):
        self.read_power_task.start()
        self.button_power["text"] = "Turn OFF"

    def on_set_angle(self):
        self.set_angle_task.start()

    def on_set_wavelength(self):
        self.set_wavelength_task.start()

    def on_set_actuator_position(self):
        self.set_actuator_position_task.start()

    def on_home_actuator(self):
        self.home_actuator_task.start()
    
    def on_home_ndfilter(self):
        self.home_ndfilter_task.start()

    def browse_actuator_calibration_file(self):
        file_path = askopenfilename(
            title="Select Actuator Calibration File", filetypes=(("csv files", "*.csv"),))
        if file_path:
            VARIABLES.var_entry_actuator_calibration_file.set(file_path)
