__author__ = 'gkour'

import tkinter as tk
from visualization.gui import OriginGUI
from configsimulator import ConfigSimulator


class OriginApp:

    def __init__(self, master):
        self.master = master

        # Set up the GUI part
        self.gui = OriginGUI(master)

        self.periodic_call()

    def periodic_call(self):
        self.gui.process_incoming_msg()
        try:
            self.master.after(ConfigSimulator.UI_UPDATE_INTERVAL, self.periodic_call)
        except:
            print("Periodic call exception.")


if __name__ == '__main__':
    root = tk.Tk()
    client = OriginApp(root)
    root.mainloop()
