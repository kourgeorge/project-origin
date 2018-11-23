import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

plt.style.use(['seaborn-paper'])


class Dashboard:
    def __init__(self):
        plt.ion()

        mpl.rcParams['toolbar'] = 'None'
        self._fig_step = plt.figure(figsize=(9, 6), dpi=120, facecolor='w')
        self._fig_step.canvas.set_window_title('Origin Dashboard')
        self._fig_step_pop = self._fig_step.add_subplot(221)
        self._fig_step_pop.set_ylabel('Population Size')
        self._fig_step_age = self._fig_step.add_subplot(222)
        self._fig_step_age.set_ylabel('Avg Population Age')
        self._line_pop, = self._fig_step_pop.plot([], [], '-')
        self._line_age, = self._fig_step_age.plot([], [], '-')
        self._fig_step_creat_loc = self._fig_step.add_axes([0.1, 0.1, 0.4, 0.05])
        self._fig_step_food_loc = self._fig_step.add_axes([0.1, 0.25, 0.4, 0.05])
        self._fig_step_action = self._fig_step.add_subplot(224)

    def update_epoch_dash(self, epoch_stats_df):
        creatures_dist = np.asarray(epoch_stats_df['Creatures'].iloc[-1])
        self._fig_step_creat_loc.clear()
        self._fig_step_creat_loc.imshow(creatures_dist[np.newaxis, :], cmap="Purples", aspect="auto")
        self._fig_step_creat_loc.set_title('Creatures Location')

        food_supply = np.asarray(epoch_stats_df['Food Supply'].iloc[-1])
        self._fig_step_food_loc.clear()
        self._fig_step_food_loc.imshow(food_supply[np.newaxis, :], cmap="Blues", aspect="auto")
        self._fig_step_food_loc.set_title('Food Supply')

        actions_dist = epoch_stats_df['Action Dist [LREMF]'].iloc[-1]
        self._fig_step_action.clear()
        self._fig_step_action.pie(actions_dist, labels=['Left', 'Right', 'Eat', 'Mate', 'Fight'],
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
