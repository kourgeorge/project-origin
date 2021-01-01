__author__ = 'pkour'

from config import ConfigPhysics


class Sound:
    def __init__(self, creature, time, syllable='Bla', lasting_time=ConfigPhysics.SOUND_LASTING_TIME):
        self._creature = creature
        self._initial_time = time
        self._syllable = syllable
        self._end_time = time + lasting_time

    def creature(self):
        return self._creature

    def get_end_time(self):
        return self._end_time
