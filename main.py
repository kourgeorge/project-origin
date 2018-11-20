__author__ = 'gkour'

from universe import Universe
from creature import Creature
from config import Config
import numpy as np
import datacollector
import aiq
import utils
from collections import OrderedDict


def main():
    universe = Universe()
    step_stats = collect_step_stats(universe)
    print_step_stats(step_stats)
    print_epoch_stats(universe)

    while universe.pass_time():
        if universe.num_creatures() == 0:
            step_stats = collect_step_stats(universe)
            print_step_stats(step_stats)
            print_epoch_stats(universe)
            return

        universe.give_food(round(universe.num_creatures() * 0.7))
        step_stats = collect_step_stats(universe)
        print_step_stats(step_stats)

        if universe.get_time() % 10 == 0:
            print_epoch_stats(universe)

        datacollector.action_log = np.zeros_like(datacollector.action_log)


# if (len(universe.get_all_creatures())) == 1:
#    print(universe.get_all_creatures()[0].dna())


def collect_step_stats(universe):
    return OrderedDict([
        ('Time', universe.get_time()),
        ('Population', universe.num_creatures()),
        ('IDs', Creature.counter),
        ('Age', np.round(np.nanmean([creature.age() for creature in universe.get_all_creatures()]))),
        ('MaxAge', np.round(np.nanmean([creature.max_age() for creature in universe.get_all_creatures()]), 2)),
        ('Hidden Layer',
            np.round(np.mean([creature.brain_hidden_layer() for creature in universe.get_all_creatures()]), 2)),
        ('Learn Freq',
            np.round(np.mean([creature.learning_frequency() for creature in universe.get_all_creatures()]), 2)),
        ('Learn Rate', np.round(np.mean([creature.learning_rate() for creature in universe.get_all_creatures()]) * (
                1 / Config.ConfigBrain.LEARNING_RATE), 2)),
        ('Vision Range', np.round(np.mean([creature.vision_range() for creature in universe.get_all_creatures()]), 2)),
        ('Artificial IQ', aiq.population_aiq_dist(universe.get_all_creatures()))
    ])


def print_step_stats(step_stats):

    for (key, value) in step_stats.items():
        print('{}: {}'.format(key, value), end=' | ')

    print()


def log_step_stats(step_stats):
    file_path = './log/log.csv'
    utils.log(file_path, step_stats)


def print_epoch_stats(universe):
    # print(universe.space(), end='\t')
    print('Death Cause [Fa Fi E]: ' + str(datacollector.death_cause))
    datacollector.death_cause = np.zeros_like(datacollector.death_cause)

    print('Food Supply: ' + str(universe.get_food_distribution()))
    print('Creatures: ' + str(universe.get_creatures_distribution()))
    print('Action Dist [LREMF]: ' + str(np.round(np.array(datacollector.action_log) / sum(datacollector.action_log), 2)))
    # energy = [creature.energy() for creature in universe.get_all_creatures()]
    # print(np.histogram(energy))


if __name__ == '__main__':
    main()
