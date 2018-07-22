import numpy as np
import utils


class Evolution:

    @staticmethod
    def mix_dna(dna1, dna2):
        mixed = dna1 + dna2 + np.random.normal(0, 0.3, len(dna1))
        return utils.softmax(mixed)


