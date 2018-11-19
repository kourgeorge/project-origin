__author__ = 'gkour'

from cell import Cell
from config import Config


class Space:
    def __init__(self, space_size):
        self._space_size = space_size
        self._grid = []
        for i in range(space_size):
            self._grid.append(Cell(i))

    def grid(self):
        return self._grid

    def get_state_in_coord(self, coord, vision_range):
        state = []
        for i in range(coord - vision_range, coord + vision_range + 1): #range(-1,1) = [-1,0]
            if i < 0 or i >= Config.ConfigPhysics.SPACE_SIZE:
                state.extend([-1, -1])
            else:
                cell = self._grid[i]
                state.extend([cell.get_food(), cell.num_creatures()])
        return state

    def get_all_creatures(self):
        all_creatures = [cell.creatures() for cell in self._grid]
        flat_list = []
        for sublist in all_creatures:
            for item in sublist:
                flat_list.append(item)

        return flat_list

    def get_food_distribution(self):
        return [cell.get_food() for cell in self._grid]

    def __str__(self):
        string = ''
        for cell in self._grid:
            string = string + str(cell) + ' '

        return string
