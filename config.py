__author__ = 'gkour'


class Config:
    LOG_FILE_PATH = './log/log.csv'
    UI_UPDATE_INTERVAL = 200 #ms

    class ConfigPhysics:
        SPACE_SIZE = 50
        NUM_FATHERS = 30
        ETERNITY = 100000
        FOOD_CREATURE_RATIO = 0.5

    class ConfigBiology:
        RACE_NAME = 'mango'
        BASE_DYING_AGE = 80
        DNA_SIZE = 6
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 100
        MATE_ENERGY = int(INITIAL_ENERGY / 4)
        MATURITY_AGE = int(BASE_DYING_AGE / 5)
        BASE_LEARN_FREQ = 20
        BASE_VISION_RANGE = 3
        MEAL_SIZE = 6
        WORK_ENERGY = 3

    class ConfigBrain:
        BASE_GAMMA = 0.9
        BASE_LEARNING_RATE = 1e-4
        BASE_HIDDEN_LAYER_SIZE = 6


