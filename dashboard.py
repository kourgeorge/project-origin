__author__ = 'gkour'

import matplotlib.pyplot as plt
import numpy as np
from creature_actions import Actions
from config import Config


class Dashboard:

    def __init__(self):

        self._fig = plt.figure(figsize=(9, 5), dpi=120, facecolor='w')
        self._fig.canvas.set_window_title('Origin Dashboard')
        self._axes_pop = self._fig.add_subplot(221)
        self._axes_pop.set_ylabel('Population Size')
        self._line_pop, = self._axes_pop.semilogy([], [], '-', label=self._axes_pop.yaxis.label.get_text())
        self._axes_age = self._axes_pop.twinx()
        self._axes_age.set_ylabel('AVG Age')
        self._line_age, = self._axes_age.plot([], [], 'y-', label=self._axes_age.yaxis.label.get_text())
        self._axes_pop.legend([self._line_pop, self._line_age],
                              [self._line_pop.get_label(), self._line_age.get_label()], loc=0)

        self._axes_aiq = self._fig.add_subplot(222)
        self._axes_aiq.set_ylabel('Population AIQ')
        self._line_aiq, = self._axes_aiq.plot([], [], '-', label=self._axes_aiq.yaxis.label.get_text())

        self._fig_creatures_loc = self._fig.add_axes([0.05, 0.1, 0.2, 0.3])
        self._fig_creatures_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_creatures_loc.xaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc = self._fig.add_axes([0.26, 0.1, 0.2, 0.3])
        self._fig_food_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc.xaxis.set_major_locator(plt.NullLocator())
        self._fig_action = self._fig.add_subplot(236)
        self._fig_death = self._fig.add_subplot(2, 6, 10)

    def update_epoch_dash(self, epoch_stats_df):
        if epoch_stats_df is None or epoch_stats_df.empty:
            return
        ## Action Dist Pie
        death_cause = np.mean(epoch_stats_df['DeathCause'], axis=0)
        self._fig_death.clear()
        self._fig_death.pie(death_cause, labels=['Fatigue', 'Fight', 'Elderly'],
                             startangle=90, autopct='%1.1f%%')

    def update_step_dash(self, step_stats_df):
        if step_stats_df is None or step_stats_df.empty:
            return
        self._line_pop.set_xdata(step_stats_df['Time'])
        self._line_pop.set_ydata(step_stats_df['Population'])

        self._line_age.set_xdata(step_stats_df['Time'])
        self._line_age.set_ydata(step_stats_df['Age'])

        self._line_aiq.set_xdata(step_stats_df['Time'])
        self._line_aiq.set_ydata(step_stats_df['AIQ'])

        self._fig.canvas.draw()
        self._fig.canvas.flush_events()
        self._axes_pop.relim()
        self._axes_pop.autoscale_view()
        self._axes_age.relim()
        self._axes_age.autoscale_view()
        self._axes_aiq.relim()
        self._axes_aiq.autoscale_view()

        ## Creatures Dist
        creatures_dist = np.asarray(step_stats_df['CreaturesDist'].iloc[-1])
        self._fig_creatures_loc.clear()
        self._fig_creatures_loc.imshow(creatures_dist, cmap="Purples", aspect="auto", vmin=0, vmax=30)
        self._fig_creatures_loc.set_title('Creatures Location')
        self._fig_creatures_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_creatures_loc.xaxis.set_major_locator(plt.NullLocator())

        ## Food Supply
        food_supply = np.asarray(step_stats_df['FoodDist'].iloc[-1])
        self._fig_food_loc.clear()
        self._fig_food_loc.imshow(food_supply, cmap="Greens", aspect="auto", vmin=0, vmax=100)
        self._fig_food_loc.set_title('Food Dist')
        self._fig_food_loc.yaxis.set_major_locator(plt.NullLocator())
        self._fig_food_loc.xaxis.set_major_locator(plt.NullLocator())

        ## Action Dist Pie
        actions_dist = np.mean(step_stats_df['ActionDist'].tail(Config.Batch_SIZE).values, axis=0)
        self._fig_action.clear()
        self._fig_action.pie(actions_dist, labels=Actions.get_available_action_str(),
                             startangle=90, autopct='%1.1f%%')

    def get_figure(self):
        return self._fig


