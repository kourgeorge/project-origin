import numpy as np
from sklearn.preprocessing import normalize


def random_dna(dna_size):
    dna = np.random.normal(size=dna_size)
    return softmax(dna)


def softmax(x):
    """
    Compute softmax values for each sets of scores in x.

    Rows are scores for each class.
    Columns are predictions (samples).
    """
    #x = normalize(np.reshape(x, (1, -1)), norm='l2')[0]
    scoreMatExp = np.exp(np.subtract(x,max(x)))
    if np.isinf(np.sum(scoreMatExp)):
        x = 1
    return scoreMatExp / scoreMatExp.sum(0)


def roll_fight(energy1, energy2):
    dist = softmax([energy1, energy2])
    return np.random.choice(a=[-1, 1], p=dist)
