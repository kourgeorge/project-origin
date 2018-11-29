__author__ = 'gkour'

import sim_runner
from visualization.dashboard import Dashboard
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, Scale
import matplotlib.pyplot as plt
from config import Config
import threading


plt.style.use('seaborn-paper')
LARGE_FONT = ("Verdana", 12)


class OriginGUI:

    def __init__(self, master, queue, *args, **kwargs):
        tk.Tk.wm_title(master, "Project Origin")
        # tk.Tk.iconbitmap(self,default="")

        self.master = master
        self.queue = queue
        container = tk.Frame(master)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._simulation_page = SimulationPage(container, master, queue)
        self._simulation_page.grid(row=0, column=0, sticky="nsew")
        self._simulation_page.tkraise()

    def refresh_data(self, msg):
        self._simulation_page.refresh_data(msg)

    def processIncoming(self):
        """Handle all messages currently in the queue, if any."""
        self._simulation_page.check_handle_sim_end()
        while self.queue.qsize():
            try:
                self.refresh_data(self.queue.get(0))
            except Exception as exp:
                print(str(exp))
                pass


class SimulationPage(tk.Frame):

    def __init__(self, parent, controller, queue):
        self._dashboard = Dashboard()
        self.controller = controller
        self.queue = queue
        self.sim_thread = None

        tk.Frame.__init__(self, parent, bg='white')
        title_label = tk.Label(self, text="Project Origin Dashboard", font=LARGE_FONT, foreground='blue', bg='white')
        title_label.pack(pady=10, padx=10)

        self.s = ttk.Style()
        self.s.theme_use('vista')

        self.status_label = tk.Label(self, text="Simulator ready", bg='white')
        self.status_label.pack(pady=10, padx=10)

        self.start_sim_btn = ttk.Button(self, text="Start Simulation",
                                        command=lambda: self.start_simulation())

        self.start_sim_btn.pack()
        self.food_creature_scale = Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1, bg='white',
                                         command=lambda x: self.set_food_creature_ratio(x))
        self.food_creature_scale.set(Config.ConfigPhysics.FOOD_CREATURE_RATIO)
        self.food_creature_scale.pack()

        dash_fig = self._dashboard.get_figure()

        canvas = FigureCanvasTkAgg(dash_fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def refresh_data(self, statistics):
        self._dashboard.update_step_dash(statistics.step_stats_df)
        self._dashboard.update_epoch_dash(statistics.epoch_stats_df)

    def start_simulation(self):
        self.status_label['text'] = "Simulation Started!"
        self.start_sim_btn['state'] = tk.DISABLED

        self.sim_thread = threading.Thread(target=sim_runner.run, args=[self.queue])
        self.sim_thread.daemon = True
        self.sim_thread.start()

    def check_handle_sim_end(self):
        if self.sim_thread is not None and not self.sim_thread.isAlive():
            self.start_sim_btn['state'] = tk.ACTIVE
            self.status_label['text'] = 'Simulation Ended'


    @staticmethod
    def set_food_creature_ratio(new):
        Config.ConfigPhysics.FOOD_CREATURE_RATIO = float(new)

