from universe import Universe
import numpy as np
import utils

num_fathers = 10
space_size = 10
universe = Universe(num_fathers)

time = 0
while time < 10000000:
    universe.give_food()
    #print(universe.space())
    universe.pass_time()
    time += 1

    if time % 500 == 0:
        dna_agg = []
        dna_agg = [creature.dna() for creature in universe.get_all_creatures()]
        print(str(len(universe.get_all_creatures())))
        print(np.mean(dna_agg, axis=0))
