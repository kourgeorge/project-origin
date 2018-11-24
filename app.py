__author__ = 'gkour'

import tkinter as tk
from queue import Queue
from gui import OriginGUI


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
        self.gui = OriginGUI(master, self.msg_queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        #self.thread1 = threading.Thread(target=run)
        #self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodic_call()

    def periodic_call(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        # if not self.running:
        #     # This is the brutal stop of the system. You may want to do
        #     # some cleanup before actually shutting it down.
        #     import sys
        #     sys.exit(1)
        self.master.after(200, self.periodic_call)

    def endApplication(self):
        self.running = 0


if __name__ == '__main__':
    root = tk.Tk()
    client = OriginApp(root)
    root.mainloop()
