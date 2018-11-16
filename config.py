__author__ = 'gkour'


class Config:
    class ConfigPhysics:
        SPACE_SIZE = 5
        NUM_FATHERS = 10
        ETERNITY = 100000

    class ConfigBiology:
        RACE_NAME = 'mango'
        DYING_AGE = 20
        DNA_SIZE = 5
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 20
        MATE_ENERGY = INITIAL_ENERGY / 2
        MATURITY_AGE = 0
        WISDOM_INTERVAL = 5

    class ConfigBrain:
        GAMMA = 1
        LEARNING_RATE = 1e-4
        HIDDEN_LAYER_SIZE = 32
        ACTION_SIZE = 5
        STATE_SIZE = 4


