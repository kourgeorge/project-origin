from universe import Universe
import tensorflow as tf
import numpy as np
import log


def main():

    universe = Universe()

    while universe.pass_time():

        universe.give_food(1)

        print(str(universe.num_creatures()), end=' ')
        if universe.num_creatures() == 0:
            return

        if universe.get_time() % 10 == 0:

            print(universe.space(), end='\t')
            print("[LREMF]:" + str(np.array(log.action_log)/sum(log.action_log)))
            # energy = [creature.energy() for creature in universe.get_all_creatures()]
            # print(np.histogram(energy))

        #if (len(universe.get_all_creatures())) == 1:
        #    print(universe.get_all_creatures()[0].dna())


if __name__ == '__main__':
    main()
