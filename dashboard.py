import matplotlib.pyplot as plt
import numpy as np


class Dashboard:
    def __init__(self):
        plt.ion()

        self._fig_step = plt.figure()
        self._fig_step_pop = self._fig_step.add_subplot(221)
        self._fig_step_pop.set_ylabel('Population Size')
        self._fig_step_age = self._fig_step.add_subplot(222)
        self._fig_step_age.set_ylabel('Avg Population Age')
        self._line_pop, = self._fig_step_pop.plot([], [], '-')
        self._line_age, = self._fig_step_age.plot([], [], '-')
        self._fig_step_loc = self._fig_step.add_subplot(223)
        self._fig_step_action = self._fig_step.add_subplot(224)

    def update_epoch_dash(self, epoch_stats_df):
        creatures_dist = np.asarray(epoch_stats_df['Creatures'].iloc[-1])
        self._fig_step_loc.clear()
        self._fig_step_loc.imshow(creatures_dist[np.newaxis, :], cmap="plasma", aspect="auto")
        self._fig_step_loc.set_title('Creatures Location')

        actions_dist = epoch_stats_df['Action Dist [LREMF]'].iloc[-1]
        self._fig_step_action.clear()
        self._fig_step_action.pie(actions_dist, labels=['left', 'Right', 'Eat', 'Mate', 'Fight'],
                                  startangle=90, autopct='%1.1f%%')
        self._fig_step_action.set_title('Action Distribution')

    def update_step_dash(self, step_stats_df):
        self._line_pop.set_xdata(step_stats_df.index.values)
        self._line_pop.set_ydata(step_stats_df['Population'])

        self._line_age.set_xdata(step_stats_df.index.values)
        self._line_age.set_ydata(step_stats_df['Age'])

        self._fig_step.canvas.draw()
        self._fig_step.canvas.flush_events()
        self._fig_step_pop.relim()
        self._fig_step_pop.autoscale_view()
        self._fig_step_age.relim()
        self._fig_step_age.autoscale_view()
