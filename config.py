__author__ = 'gkour'


class Config:
    LOG_FILE_PATH = './log/log.csv'

    class ConfigPhysics:
        SPACE_SIZE = 50
        NUM_FATHERS = 20
        ETERNITY = 100000

    class ConfigBiology:
        RACE_NAME = 'mango'
        BASE_DYING_AGE = 80
        DNA_SIZE = 5
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 100
        MATE_ENERGY = INITIAL_ENERGY / 4
        MATURITY_AGE = BASE_DYING_AGE / 5
        BASE_LEARN_FREQ = 6
        BASE_VISION_RANGE = 3

    class ConfigBrain:
        GAMMA = 1
        BASE_LEARNING_RATE = 17 * 1e-4
        BASE_HIDDEN_LAYER_SIZE = 3
        ACTION_SIZE = 5

