from universe import Universe
import tensorflow as tf
import numpy as np
from Config import Config
import log


def main():

    tf.reset_default_graph()

    num_fathers = 10
    space_size = 5
    Config.optimizer = tf.train.GradientDescentOptimizer(learning_rate=Config.lr)
    universe = Universe(num_fathers, space_size)

    time = 0
    Config.sess = tf.Session()
    Config.sess.run(tf.global_variables_initializer())

    while time < 10000:

        if time < 100:
            universe.give_food(2)

        print(str(universe.num_creatures()), end=' ')
        if universe.num_creatures() == 0:
            vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
            return

        universe.pass_time()
        time += 1

        if time % 10 == 0:
            #dna_agg = []
            #dna_agg = [creature.dna() for creature in universe.get_all_creatures()]
            #print(np.mean(dna_agg, axis=0))
            print(universe.space(), end='\t')
            print("action: dist:" + str(np.array(log.action_log)/sum(log.action_log)))
            # energy = [creature.energy() for creature in universe.get_all_creatures()]
            # print(np.histogram(energy))

        #if (len(universe.get_all_creatures())) == 1:
        #    print(universe.get_all_creatures()[0].dna())


if __name__ == '__main__':
    main()