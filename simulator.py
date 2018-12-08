__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing
from configsimulator import ConfigSimulator
import time
import threading
from enum import Enum


class SimState(Enum):
    STOPPED = "Simulation Terminated"
    INITIALIZING = "Simulation Initialized"
    RUNNING = "Simulation Running"
    STOPPING = "Simulation Terminating"


class Simulator:
    def __init__(self, queue=None):
        self._thread = None
        self._status = SimState.STOPPED
        self._msg_queue = queue

    def run(self):
        self._status = SimState.INITIALIZING
        stats = Stats()
        universe = Universe(ConfigSimulator.RACES, stats)

        self._status = SimState.RUNNING
        self._report_state()

        while self._status == SimState.RUNNING and universe.pass_time():
            stats.accumulate_step_stats(universe)
            printing.print_step_stats(stats)
            self._report(stats)
            stats.initialize_inter_step_stats()

            if universe.get_time() % ConfigSimulator.BATCH_SIZE == 0:
                stats.accumulate_epoch_stats(universe)
                printing.print_epoch_stats(stats)

        if ConfigSimulator.CSV_LOGGING:
            printing.dataframe2csv(stats.step_stats_df,
                                   ConfigSimulator.CSV_FILE_PATH.format(time.strftime("%Y%m%d-%H%M%S")))

        self._status = SimState.STOPPED
        self._report_state()

    def status(self):
        return self._status

    def stop(self):
        self._status = SimState.STOPPING
        if self._thread is None or not self._thread.isAlive():
            self._status = SimState.STOPPING
        else:
            self._status = SimState.STOPPING
        self._report_state()

    def _report(self, msg):
        if self._msg_queue:
            self._msg_queue.put(msg)

    def _report_state(self):
        self._msg_queue.put(self._status)

    def run_in_thread(self):
        self._status = SimState.INITIALIZING
        self._report_state()
        self._thread = threading.Thread(target=self.run)
        self._thread.start()


if __name__ == '__main__':
    sim = Simulator()
    sim.run()
