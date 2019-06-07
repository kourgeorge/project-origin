__author__ = 'gkour'

from simulator import Simulator, SimState
from visualization.dashboard import Dashboard
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, Scale
import matplotlib.pyplot as plt
from config import ConfigPhysics
import sys
from queue import Queue

plt.style.use('seaborn-paper')
LARGE_FONT = ("Verdana", 12)


class OriginGUI:

    def __init__(self, master, *args, **kwargs):
        tk.Tk.wm_title(master, "Project Origin")
        #master.iconbitmap(default="visualization/originicon.bmp")

        self.master = master
        self.msg_queue = Queue()

        container = tk.Frame(master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._simulation_page = SimulationPage(container, master, self.msg_queue)
        self._simulation_page.grid(row=0, column=0, sticky="nsew")
        self._simulation_page.tkraise()

    def refresh_data(self, msg):
        self._simulation_page.refresh_data(msg)

    def process_incoming_msg(self):
        """Handle all messages currently in the queue, if any."""
        while self.msg_queue.qsize():
            try:
                self.refresh_data(self.msg_queue.get())
            except Exception as exp:
                print(str(exp))
                pass


class SimulationPage(tk.Frame):

    def __init__(self, parent, controller, queue):
        self._dashboard = Dashboard()
        self.controller = controller
        self.simulator = Simulator(queue)
        self.window_closed = False

        tk.Frame.__init__(self, parent, bg='white')
        title_label = tk.Label(self, text="Project Origin Dashboard", font=LARGE_FONT, foreground='blue', bg='white')
        title_label.pack(pady=10, padx=10)

        self.s = ttk.Style()
        self.s.theme_use('vista')

        self.status_label = tk.Label(self, text="Simulator Ready.", bg='white')
        self.status_label.pack(pady=10, padx=10)

        self.sim_btn = ttk.Button(self, text="Start Simulation", command=lambda: self.on_simulation_btn_click())

        self.sim_btn.pack()
        self.food_creature_scale = Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, bg='white',
                                         command=lambda x: self.set_food_creature_ratio(x))
        self.food_creature_scale.set(ConfigPhysics.FOOD_CREATURE_RATIO)
        self.food_creature_scale.pack()

        dash_fig = self._dashboard.get_figure()

        canvas = FigureCanvasTkAgg(dash_fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        controller.protocol("WM_DELETE_WINDOW", self.close_window_event)

        self.on_simulation_btn_click()

    def close_window_event(self):
        self.stop_simulation()
        self.window_closed = True
        if self.simulator.status() == SimState.IDLE:
            self.close_window()

    def close_window(self):
        self.controller.destroy()
        sys.exit()

    def refresh_data(self, msg):
        if type(msg) == SimState:
            print(msg.value)
            if msg == SimState.IDLE:
                self.sim_btn['text'] = 'Start Simulation'
                self.sim_btn['state'] = tk.ACTIVE
                if self.window_closed:
                    self.close_window()
            self.status_label['text'] = str(msg.value)
        else:
            self._dashboard.update_step_dash(msg.step_stats_df)
            self._dashboard.update_epoch_dash(msg.epoch_stats_df)

    def on_simulation_btn_click(self):
        if self.sim_btn['text'] == 'Start Simulation':
            self.start_simulation()
            self.sim_btn['text'] = 'Stop Simulation'
        else:
            self.stop_simulation()
            self.sim_btn['state'] = tk.DISABLED

    def stop_simulation(self):
        self.simulator.stop()
        self.status_label['text'] = "Simulation Interrupted. Stopping..."

    def start_simulation(self):
        self.simulator.run_in_thread()

    @staticmethod
    def set_food_creature_ratio(new):
        ConfigPhysics.FOOD_CREATURE_RATIO = float(new)
