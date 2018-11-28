__author__ = 'gkour'


class Config:
    LOG_FILE_PATH = './log/log.csv'
    Batch_SIZE = 10
    UI_UPDATE_INTERVAL = 200 #ms

    class ConfigPhysics:
        SPACE_SIZE = 20
        NUM_FATHERS = 200
        ETERNITY = 100000
        SLIPPERY_SPACE = False
        FOOD_CREATURE_RATIO = 0
        INITIAL_FOOD_AMOUNT = NUM_FATHERS * 10 ** 4

    class ConfigBiology:
        RACE_NAME = 'mango'
        BASE_DYING_AGE = 800
        DNA_SIZE = 6
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 50
        MATE_ENERGY = int(INITIAL_ENERGY / 4)
        MATURITY_AGE = 20 #int(BASE_DYING_AGE / 5)
        BASE_LEARN_FREQ = 20
        BASE_VISION_RANGE = 2
        MEAL_SIZE = 6
        WORK_ENERGY = 3

    class ConfigBrain:
        BASE_GAMMA = 0.9
        BASE_LEARNING_RATE = 1e-3
        BASE_HIDDEN_LAYER_SIZE = 6
        MODEL_PATH = './model/model'


