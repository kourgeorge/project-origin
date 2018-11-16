from universe import Universe
from creature import Creature
from config import Config
import numpy as np
import log


def main():
    universe = Universe()

    while universe.pass_time():

        if universe.num_creatures() == 0:
            return

        current_time = universe.get_time()
        universe.give_food(Config.ConfigPhysics.NUM_FATHERS)

        print(str(current_time) + ' - Population: ' + str(universe.num_creatures()), end='\t - ')
        print('IDs:' + str(Creature.counter), end='\t - ')
        mean_age = np.round(np.mean([creature.age() for creature in universe.get_all_creatures()]))
        print('Mean age: ' + str(mean_age), end='\t - ')
        print('Death Cause [Fa Fi E]: ' + str(log.death_cause))
        log.death_cause = [0, 0, 0]

        if current_time % 10 == 0:
            # print(universe.space(), end='\t')
            print('Food Supply: ' + str(universe.get_food_distribution()))
            print('Action Dist [LREMF]: ' + str(np.round(np.array(log.action_log) / sum(log.action_log), 2)))
            # energy = [creature.energy() for creature in universe.get_all_creatures()]
            # print(np.histogram(energy))

            log.action_log = np.zeros_like(log.action_log)

        # if (len(universe.get_all_creatures())) == 1:
        #    print(universe.get_all_creatures()[0].dna())


if __name__ == '__main__':
    main()
