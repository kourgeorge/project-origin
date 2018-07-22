from universe import Universe
import numpy as np

num_fathers = 50
space_size = 10
universe = Universe(num_fathers)

time = 0
while time < 10000:

    if time < 100:
        universe.give_food()

    print(str(len(universe.get_all_creatures())), end=' ')

    universe.pass_time()
    time += 1

    if time % 100 == 0:
        dna_agg = []
        dna_agg = [creature.dna() for creature in universe.get_all_creatures()]
        print(np.mean(dna_agg, axis=0))
        print(universe.space())
        #energy = [creature.energy() for creature in universe.get_all_creatures()]
        #print(np.histogram(energy))

    if (len(universe.get_all_creatures())) == 1:
        print(universe.get_all_creatures()[0].dna())
