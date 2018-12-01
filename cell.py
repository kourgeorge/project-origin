__author__ = 'gkour'


class Cell:
    def __init__(self, coord):
        self._coord = coord
        self._creatures = []
        self._food = 0

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

    def get_coord(self):
        return self._coord

    def find_nearby_creature(self, creature):
        if len(self._creatures) < 2:
            return None
        for i in range(len(self._creatures)):
            if self._creatures[i] != creature:
                return self._creatures[i]

    def find_nearby_creature_from_same_race(self, creature):
        for i in range(len(self._creatures)):
            if self._creatures[i].race_name() == creature.race_name() and self._creatures[i] != creature:
                return self._creatures[i]
        return None

    def find_nearby_creature_from_different_race(self, creature):
        for i in range(len(self._creatures)):
            if self._creatures[i].race_name() != creature.race_name() and self._creatures[i] != creature:
                return self._creatures[i]
        return None

    def creatures(self):
        return self._creatures

    def energy_level(self):
        return sum([creature.energy() for creature in self.creatures()])

    def race_energy_level(self, race):
        return sum([creature.energy() for creature in self.creatures() if creature.race_name() == race.race_name()])


    def num_creatures(self):
        return len(self._creatures)

    def __str__(self):
        return str(self._coord) + ':F(' + str(self.get_food()) + ')C(' + str(len(self.creatures())) + ') '
