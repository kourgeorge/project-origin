# The code for changing pages was derived from: http://stackoverflow.com/questions/7546050/switch-between-two-frames-in-tkinter
# License: http://creativecommons.org/licenses/by-sa/3.0/

import matplotlib
import sim_runner
from dashboard import Dashboard
from stats import Stats
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana", 12)


class OriginApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Project Origin")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SimulationPage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button3 = ttk.Button(self, text="Graph Page",
                             command=lambda: controller.show_frame(SimulationPage))
        button3.pack()


class SimulationPage(tk.Frame):
    dash = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        start_sim = ttk.Button(self, text="Start Simulation",
                               command=lambda: sim_runner.run_in_thread())
        start_sim.pack()

        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 6, 1, 3, 8, 9, 3, 5])

        SimulationPage.dash = Dashboard()
        dash_fig = SimulationPage.dash.get_figure()

        canvas = FigureCanvasTkAgg(dash_fig, self)
        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @staticmethod
    def update_dash():
        print("In Update Dashhhhhhhhhhhhh")
        if Stats.ready_for_ui:
            SimulationPage.dash.update_step_dash(Stats.step_stats_df)
        app.after(1000, SimulationPage.update_dash)

app = OriginApp()
app.after(1000, SimulationPage.update_dash)
app.mainloop()
