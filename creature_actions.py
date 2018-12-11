from enum import Enum


class AutoNumber(Enum):
    def __new__(cls):
        value = len(cls.__members__)  # note no + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class Actions(AutoNumber):
    LEFT = ()
    RIGHT = ()
    UP = ()
    DOWN = ()
    EAT = ()
    MATE = ()
    FIGHT = ()
    WORK = ()
    DIVIDE = ()
    VOCALIZE = ()

    @staticmethod
    def get_all_actions():
        return [Actions.LEFT, Actions.RIGHT, Actions.UP, Actions.DOWN, Actions.EAT, Actions.MATE, Actions.FIGHT,
                Actions.WORK, Actions.DIVIDE, Actions.VOCALIZE]

    def __str__(self):
        return str(self.name)

    @staticmethod
    def num_actions():
        return len(Actions.get_all_actions())

    @staticmethod
    def is_legal(action):
        if action in Actions.get_all_actions():
            return True
        return False

    @staticmethod
    def index_to_enum(index):
        return Actions.get_all_actions()[index]

    @staticmethod
    def enum_to_index(action):
        return Actions.get_all_actions().index(action)

    @staticmethod
    def get_actions_str():
        return [str(action) for action in Actions.get_all_actions()]
