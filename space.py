from cell import Cell


class Space:
    def __init__(self, space_size):
        self._space_size = space_size
        self._grid = []
        for i in range(space_size):
            self._grid.append(Cell(i))

    def grid(self):
        return self._grid

    def get_state_in_coord(self, coord):
        cell = self._grid[coord]
        return [cell.get_food(), cell.num_creatures()]

    def get_all_creatures(self):
        all_creatures = [cell.creatures() for cell in self._grid]
        flat_list = []
        for sublist in all_creatures:
            for item in sublist:
                flat_list.append(item)

        return flat_list

    def __str__(self):
        string = ''
        for cell in self._grid:
            string = string + str(cell) + ' '

        return string

