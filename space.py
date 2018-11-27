__author__ = 'gkour'

from cell import Cell
import numpy as np
from itertools import chain


class Space:
    def __init__(self, space_size):
        self._space_size = space_size
        self._grid = []
        for i in range(space_size):
            self._grid = [[Cell((i, j)) for j in range(self._space_size)] for i in range(self._space_size)]

    def grid(self):
        return self._grid

    def insert_creature(self, creature, coord):
        if not self.valid_coord(coord):
            print("Exception: bad coordinated in space.insert_creature")
            return None
        cell = self._grid[coord[0]][coord[1]]
        cell.insert_creature(creature)
        return cell

    def add_food(self, coord, amount):
        if not self.valid_coord(coord):
            print("Exception: bad coordinated in space.add_food")
            return None
        cell = self._grid[coord[0]][coord[1]]
        cell.add_food(amount)
        return cell

    def remove_creature(self, creature):
        x, y = creature.coord()
        self._grid[x][y].remove_creature(creature)

    def get_state_in_coord(self, coord, vision_range):
        if not self.valid_coord(coord):
            print("Exception: bad coordinated in space.get_state_in_coord")
        state_dim_size = 2 * vision_range + 1
        food_state = np.ones([state_dim_size, state_dim_size]) * -1
        creature_state = np.ones([state_dim_size, state_dim_size]) * -1

        for i in range(state_dim_size):
            for j in range(state_dim_size):
                abs_i = coord[0] - vision_range + i
                abs_j = coord[1] - vision_range + j
                if 0 <= abs_i < self._space_size and 0 <= abs_j < self._space_size:
                    food_state[i, j] = self._grid[abs_i][abs_j].get_food()
                    creature_state[i, j] = self._grid[abs_i][abs_j].num_creatures()
        # return list(chain.from_iterable(creature_state)) + list(chain.from_iterable(food_state))
        return np.stack([food_state, creature_state])

    def get_all_creatures(self):
        all_creatures = [cell.creatures() for cell in list(chain.from_iterable(self._grid))]
        flat_list = []
        for sublist in all_creatures:
            for item in sublist:
                flat_list.append(item)

        return flat_list

    def get_food_distribution(self):
        return [[self._grid[i][j].get_food() for j in range(self._space_size)] for i in range(self._space_size)]

    def get_creatures_distribution(self):
        return [[self._grid[i][j].num_creatures() for j in range(self._space_size)] for i in range(self._space_size)]

    def valid_coord(self, coord):
        x, y = coord
        return 0 <= x < self._space_size and 0 <= y < self._space_size

    def __str__(self):
        string = ''
        for cell in self._grid:
            string = string + str(cell) + ' '

        return string
