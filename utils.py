import numpy as np
from sklearn.preprocessing import normalize


def random_dna(dna_size):
    dna = np.random.normal(size=dna_size)
    dna = [0.19330016,  0.19252654,  0.21730512,  0.21953546,  0.17733273]
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
        print('Inf in softmax')
    return scoreMatExp / scoreMatExp.sum(0)


def roll_fight(energy1, energy2):
    dist = softmax([energy1, energy2])
    return np.random.choice(a=[-1, 1], p=dist)
