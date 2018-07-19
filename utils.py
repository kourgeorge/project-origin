import numpy as np



def softmax(x):
    """
    Compute softmax values for each sets of scores in x.

    Rows are scores for each class.
    Columns are predictions (samples).
    """
    scoreMatExp = np.exp(np.asarray(x))
    return scoreMatExp / scoreMatExp.sum(0)