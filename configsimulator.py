__author__ = 'gkour'

from creatures.human import Human
from creatures.humandqnbrain import HumanDQNBrain
from creatures.humantorchbrain import HumanTorchBrain, HumanTorchBrain2
from creatures.zombie import Zombie
from creatures.bacterium import Bacterium


class ConfigSimulator:
    CSV_FILE_PATH = './log/output{}.csv'
    CSV_LOGGING = False
    LOGGING_BATCH_SIZE = 10
    UI_UPDATE_INTERVAL = 200  # ms
    RACES = [HumanTorchBrain, HumanTorchBrain2]
