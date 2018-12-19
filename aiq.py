__author__ = 'gkour'

import numpy as np
from config import ConfigBiology
import utils
from creature_actions import Actions
import random


class AIQ:

    @staticmethod
    def get_population_aiq(universe):
        creatures = universe.get_all_creatures()
        sample_creatures = random.sample(creatures, utils.safe_log2(len(creatures)))
        all_aiq = [AIQ.get_creature_aiq(creature) for creature in sample_creatures]
        return np.round(utils.emptynanmean(all_aiq), 2)

    @staticmethod
    def get_population_aiq_dist(universe):
        creatures = universe.get_all_creatures()
        bounds = [ConfigBiology.BASE_LIFE_EXPECTANCY / 3, 2 * ConfigBiology.BASE_LIFE_EXPECTANCY / 3]
        young = [AIQ.get_creature_aiq(creature) for creature in creatures if creature.age() <= bounds[0]]
        adult = [AIQ.get_creature_aiq(creature) for creature in creatures if bounds[0] < creature.age() <= bounds[1]]
        old = [AIQ.get_creature_aiq(creature) for creature in creatures if bounds[1] < creature.age()]

        return np.round([utils.emptynanmean(young), utils.emptynanmean(adult), utils.emptynanmean(old)], 2)

    @staticmethod
    def get_creature_aiq(creature):
        score = 0
        scenarios = [AIQ.haven_left, AIQ.haven_right, AIQ.haven_inplace, AIQ.haven_up, AIQ.haven_down]
                     #AIQ.border_awareness_up, AIQ.border_awareness_down, AIQ.border_awareness_left, AIQ.border_awareness_right]
        w = 0
        for i in range(len(scenarios)):
            test_state, positive_test_type, expected_actions, weight = scenarios[i](creature.vision_range())
            if creature._universe.num_races() == 1:
                # delete the other race creatures entry from the state
                test_state = np.delete(test_state, obj=2, axis=0)
            w += weight
            decision = creature.index_to_enum(np.argmax(creature.brain().think(test_state)))
            if positive_test_type:
                score += weight if decision in expected_actions else 0
            else:
                score += weight if decision not in expected_actions else 0

        return score / w

    @staticmethod
    def _haven(vision_range, where):
        ''' Haven cell in current location.'''
        energy = 3
        age = 3

        food = np.zeros(shape=(2 * vision_range + 1, 2 * vision_range + 1))
        same_race_creatures = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * 20
        different_race_creatures = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * 20
        sound = np.zeros(shape=(2 * vision_range + 1, 2 * vision_range + 1))
        energy = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * energy
        age = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * age
        if where == 'INPLACE':
            food[vision_range][vision_range] = 20
            same_race_creatures[vision_range][vision_range] = 0
            different_race_creatures[vision_range][vision_range] = 0
            optimal_action = Actions.EAT
        if where == 'UP':
            food[vision_range - 1][vision_range] = 20
            same_race_creatures[vision_range - 1][vision_range] = 0
            different_race_creatures[vision_range - 1][vision_range] = 0
            optimal_action = Actions.UP
        if where == 'DOWN':
            food[vision_range + 1][vision_range] = 20
            same_race_creatures[vision_range + 1][vision_range] = 0
            different_race_creatures[vision_range + 1][vision_range] = 0
            optimal_action = Actions.DOWN
        if where == 'LEFT':
            food[vision_range][vision_range - 1] = 20
            same_race_creatures[vision_range][vision_range - 1] = 0
            different_race_creatures[vision_range][vision_range - 1] = 0
            optimal_action = Actions.LEFT
        if where == 'RIGHT':
            food[vision_range][vision_range + 1] = 20
            same_race_creatures[vision_range][vision_range + 1] = 0
            different_race_creatures[vision_range][vision_range + 1] = 0
            optimal_action = Actions.RIGHT

        return np.stack((food, sound, same_race_creatures, different_race_creatures, energy, age)), True, [
            optimal_action], 1

    @staticmethod
    def haven_inplace(vision_range):
        return AIQ._haven(vision_range, 'INPLACE')

    @staticmethod
    def haven_right(vision_range):
        return AIQ._haven(vision_range, 'RIGHT')

    @staticmethod
    def haven_left(vision_range):
        return AIQ._haven(vision_range, 'LEFT')

    @staticmethod
    def haven_up(vision_range):
        return AIQ._haven(vision_range, 'UP')

    @staticmethod
    def haven_down(vision_range):
        return AIQ._haven(vision_range, 'DOWN')

    @staticmethod
    def _border_awareness(vision_range, direction):
        energy = 3
        age = 3

        food = np.zeros(shape=(2 * vision_range + 1, 2 * vision_range + 1))
        creatures = np.zeros(shape=(2 * vision_range + 1, 2 * vision_range + 1))
        energy = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * energy
        age = np.ones(shape=(2 * vision_range + 1, 2 * vision_range + 1)) * age
        sound = np.zeros(shape=(2 * vision_range + 1, 2 * vision_range + 1))

        if direction == 'DOWN':
            food[vision_range + 1:][:] = -1
            creatures[vision_range + 1:][:] = -1
            sound[vision_range + 1:][:] = -1
            bad_action = Actions.DOWN
        if direction == 'UP':
            food[:vision_range][:] = -1
            creatures[:vision_range][:] = -1
            sound[:vision_range][:] = -1
            bad_action = Actions.UP
        if direction == 'LEFT':
            food[:][:vision_range] = -1
            creatures[:][:vision_range] = -1
            sound[:][:vision_range] = -1
            bad_action = Actions.LEFT
        if direction == 'RIGHT':
            food[:][vision_range + 1:] = -1
            creatures[:][vision_range + 1:] = -1
            sound[:][vision_range + 1:] = -1
            bad_action = Actions.RIGHT

        return np.stack((food, sound, creatures, creatures, energy, age)), False, [bad_action], 0.25

    @staticmethod
    def border_awareness_up(vision_range):
        return AIQ._border_awareness(vision_range, 'UP')

    @staticmethod
    def border_awareness_down(vision_range):
        return AIQ._border_awareness(vision_range, 'DOWN')

    @staticmethod
    def border_awareness_left(vision_range):
        return AIQ._border_awareness(vision_range, 'LEFT')

    @staticmethod
    def border_awareness_right(vision_range):
        return AIQ._border_awareness(vision_range, 'RIGHT')
