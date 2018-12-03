__author__ = 'gkour'

import tkinter as tk
from queue import Queue
from visualization.gui import OriginGUI
from configsimulator import ConfigSimulator


class OriginApp:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master
        self.msg_queue = Queue()

        # Set up the GUI part
        self.gui = OriginGUI(master, self.msg_queue)

        self.periodic_call()

    def periodic_call(self):
        self.gui.processIncoming()
        self.master.after(ConfigSimulator.UI_UPDATE_INTERVAL, self.periodic_call)


if __name__ == '__main__':
    root = tk.Tk()
    client = OriginApp(root)
    root.mainloop()
