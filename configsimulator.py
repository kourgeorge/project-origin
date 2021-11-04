__author__ = 'gkour'

#from creatures.human import Human
from creatures.humandqnbrain import HumanDQNBrain
from creatures.humanpgbrain import HumanPGBrain, HumanPGUnifiedBrain
from creatures.HumanPRLF import HumanPRLF, HumanPRLFUnifiedBrain
from creatures.zombie import Zombie
#from creatures.bacterium import Bacterium


class ConfigSimulator:
    CSV_FILE_PATH = './log/output{}.csv'
    CSV_LOGGING = False
    LOGGING_BATCH_SIZE = 10
    UI_UPDATE_INTERVAL = 100  # ms
    RACES = [Zombie, HumanPRLFUnifiedBrain]
    SIMULATION_TIME_UNIT = 0.5 #s
