__author__ = 'gkour'


class Config:
    class ConfigPhysics:
        SPACE_SIZE = 10
        NUM_FATHERS = 10
        ETERNITY = 100000

    class ConfigBiology:
        RACE_NAME = 'mango'
        DYING_AGE = 100
        DNA_SIZE = 5
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 100
        MATE_ENERGY = INITIAL_ENERGY / 4
        MATURITY_AGE = 10
        WISDOM_INTERVAL = 6

    class ConfigBrain:
        GAMMA = 1
        LEARNING_RATE = 17*1e-4
        HIDDEN_LAYER_SIZE = 3
        ACTION_SIZE = 4
        STATE_SIZE = 4


