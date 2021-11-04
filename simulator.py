__author__ = 'gkour'

from universe import Universe
from statistics import Stats
import printing
from configsimulator import ConfigSimulator
import time
import threading
from enum import Enum


class SimState(Enum):
    IDLE = "Simulation Idle"
    INITIALIZING = "Simulation Initialized"
    RUNNING = "Simulation Running"
    STOPPING = "Simulation Terminating"


class Simulator:
    def __init__(self, queue=None):
        self._thread = None
        self._status = SimState.IDLE
        self._msg_queue = queue

    def run(self):
        self._status = SimState.INITIALIZING
        self._report_state()

        stats = Stats()
        universe = Universe(ConfigSimulator.RACES, stats)

        self._status = SimState.RUNNING
        self._report_state()

        while self._status == SimState.RUNNING and universe.pass_time():
            time.sleep(ConfigSimulator.SIMULATION_TIME_UNIT)
            stats.accumulate_step_stats(universe)
            printing.print_step_stats(stats)
            self._report(stats)
            stats.initialize_inter_step_stats()

            if universe.get_time() % ConfigSimulator.LOGGING_BATCH_SIZE == 0:
                stats.accumulate_epoch_stats(universe)
                printing.print_epoch_stats(stats)

        if ConfigSimulator.CSV_LOGGING:
            printing.dataframe2csv(stats.step_stats_df,
                                   ConfigSimulator.CSV_FILE_PATH.format(time.strftime("%Y%m%d-%H%M%S")))

        self._status = SimState.IDLE
        self._report_state()

    def status(self):
        return self._status

    def stop(self):
        if self._status == SimState.IDLE:
            return
        self._status = SimState.STOPPING
        if self._thread is None or not self._thread.isAlive():
            self._status = SimState.IDLE
        else:
            self._status = SimState.STOPPING
        self._report_state()

    def _report(self, msg):
        if self._msg_queue:
            self._msg_queue.put(msg)

    def _report_state(self):
        if self._msg_queue is not None:
            self._msg_queue.put(self.status())

    def run_in_thread(self):
        self._thread = threading.Thread(target=self.run)
        self._thread.start()


if __name__ == '__main__':
    sim = Simulator()
    sim.run()
