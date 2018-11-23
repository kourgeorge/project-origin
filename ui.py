__author__ = 'gkour'

import matplotlib
import sim_runner
from dashboard import Dashboard
from stats import Stats
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from tkinter import ttk, Scale
import matplotlib.pyplot as plt
from config import Config

# s = ttk.Style()
# s.theme_use('alt')

plt.style.use('seaborn-paper')

LARGE_FONT = ("Verdana", 12)
UI_UPDATE_INTERVAL = 1000


class OriginApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Project Origin")

        # tk.Tk.iconbitmap(self,default="")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self._simulation_page = SimulationPage(container, self)
        self._simulation_page.grid(row=0, column=0, sticky="nsew")
        self._simulation_page.tkraise()

    def refresh_data(self):
        self._simulation_page.refresh_data()
        self.after(UI_UPDATE_INTERVAL, self.refresh_data)


class SimulationPage(tk.Frame):

    def __init__(self, parent, controller):
        self._dashboard = Dashboard()

        tk.Frame.__init__(self, parent)
        title_label = tk.Label(self, text="Project Origin Dashboard", font=LARGE_FONT, foreground='blue')
        title_label.pack(pady=10, padx=10)

        self.s = ttk.Style()
        self.s.theme_use('vista')

        self.status_label = tk.Label(self, text="Simulator ready")
        self.status_label.pack(pady=10, padx=10)

        self.start_sim_btn = ttk.Button(self, text="Start Simulation",
                                        command=lambda: self.start_simulation())

        self.start_sim_btn.pack()

        self.food_creature_scale = Scale(self, from_=0, to=1, orient=tk.HORIZONTAL, resolution=0.1,
                                         command=lambda x: self.set_food_creature_ratio(x))
        self.food_creature_scale.set(Config.ConfigPhysics.FOOD_CREATURE_RATIO)
        self.food_creature_scale.pack()

        dash_fig = self._dashboard.get_figure()

        canvas = FigureCanvasTkAgg(dash_fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def refresh_data(self):
        if Stats.step_ready_for_ui:
            self._dashboard.update_step_dash(Stats.step_stats_df)
        if Stats.epoch_ready_for_ui:
            self._dashboard.update_epoch_dash(Stats.epoch_stats_df)

    def start_simulation(self):
        self.status_label['text'] = "Simulation Started!"
        self.start_sim_btn['state'] = tk.DISABLED
        sim_runner.run_in_thread()

    @staticmethod
    def set_food_creature_ratio(new):
        Config.ConfigPhysics.FOOD_CREATURE_RATIO = float(new)


app = OriginApp()
app.after(UI_UPDATE_INTERVAL, app.refresh_data)
app.mainloop()
