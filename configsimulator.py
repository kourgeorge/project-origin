__author__ = 'gkour'
from creatures.human import Human
from creatures.zombie import Zombie


class ConfigSimulator:
    LOG_FILE_PATH = './log/log.csv'
    BATCH_SIZE = 10
    UI_UPDATE_INTERVAL = 200  # ms
    RACES = [Human, Zombie]