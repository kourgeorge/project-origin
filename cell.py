__author__ = 'gkour'


class Cell:
    def __init__(self, coord):
        self._coord = coord
        self._creatures = []
        self._food = 0
        self._sounds = []

    def insert_creature(self, creature):
        self._creatures.append(creature)
        return self

    def remove_creature(self, creature):
        self._creatures.remove(creature)

    def add_food(self, amount):
        self._food += amount

    def get_food(self):
        return self._food

    def remove_all_food(self):
        self._food = 0

    def remove_food(self, amount):
        self._food -= amount

    def add_sound(self, sound):
        self._sounds.append(sound)

    def remove_sounds(self, time):
        self._sounds = [s for s in self._sounds if s.get_end_time() > time]

    def get_sounds(self):
        return self._sounds

    def get_coord(self):
        return self._coord

    def creatures(self):
        return self._creatures

    def energy_level(self):
        return sum([creature.energy() for creature in self.creatures()])

    def race_energy_level(self, race):
        return sum([creature.energy() for creature in self.creatures() if creature.race_name() == race.race_name()])

    def get_state_in_cell(self, races):
        food = [self.get_food()]
        sounds = [len(self.get_sounds())]
        races_energy = [self.race_energy_level(race) for race in races]
        return food + sounds + races_energy

    def num_creatures(self):
        return len(self._creatures)

    def __str__(self):
        return str(self._coord) + ':F(' + str(self.get_food()) + ')C(' + str(len(self.creatures())) + ') '
