import numpy as np
from config import Config


action_log = np.zeros(Config.ConfigBrain.ACTION_SIZE)  #[Left Right Eat Mate Fight]
death_cause = [0, 0, 0]  #[Fatigue Fight Elderly]