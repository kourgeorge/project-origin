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
    EAT = ()
    MATE = ()
    FIGHT = ()
    WORK = ()
    DEVIDE = ()

    def __str__(self):
        return str(self.name)

    @staticmethod
    def num_actions():
        return len(Actions.get_available_list())

    @staticmethod
    def is_legal(action):
        if action in Actions.get_available_list():
            return True
        return False

    @staticmethod
    def get_available_list():
        return [Actions.LEFT, Actions.RIGHT, Actions.EAT, Actions.MATE, Actions.FIGHT]

    @staticmethod
    def get_action_from_available(index):
        return Actions.get_available_list()[index]

    @staticmethod
    def get_available_action_indx(action):
        return Actions.get_available_list().index(action)

    @staticmethod
    def get_available_action_str():
        return [str(action) for action in Actions.get_available_list()]
