## Brain

The brain is a part of every creature in project-origin.
The role of the brain is to decide on an action, given the current state of the creature, which includes information about the creature's surrounding environment and the internal state of the creature, such as age and energy.
The size of the and the nature of cues in the observed surroundings is determined by the creature senses.

There could be many types of brains, from random to complicated brain that employ neural networks and advanced learning algorithms, such as reinforcement learning.
The brain can be trained and improved by the experience of the creature.
The creature experiences are saved in the creature (limited) memory which size is defined in the creature DNA.
The frequency of brain training, is also defined in the creature dna.

Each creature may have a separate brain, or alternatively, the entire race may share the same brain which centralizes the race knowledge.
If every creature has a separate brain, it's inherited DNA may determine the structure of the brain.
In this case, the brain is trained only by the experience of the individual creature.
The structure of the race brain is predefined by the race and parts determining the brain structure in the creature's DNA are treated like [Exon](https://en.wikipedia.org/wiki/Exon).

## Creating new brains
The class [`abstractbrain.py`](/brains/abstractbrain.py) is an abstract class that each brain should implement.
