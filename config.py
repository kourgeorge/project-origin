__author__ = 'gkour'


class Config:
    class ConfigPhysics:
        SPACE_SIZE = 20
        NUM_FATHERS = 50
        ETERNITY = 100000

    class ConfigBiology:
        RACE_NAME = 'mango'
        DYING_AGE = 30
        DNA_SIZE = 5
        MOVE_ENERGY = 1
        FIGHT_ENERGY = 5
        INITIAL_ENERGY = 20
        MATE_ENERGY = INITIAL_ENERGY / 4
        MATURITY_AGE = 2
        WISDOM_INTERVAL = 5

    class ConfigBrain:
        GAMMA = 1
        LEARNING_RATE = 1e-4
        HIDDEN_LAYER_SIZE = 3
        ACTION_SIZE = 5
        STATE_SIZE = 4


