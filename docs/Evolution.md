### Evolution
Each creature has a dna  which that define it's biological structure, intelligence, senses, action tendency, etc.
For instance, how far it sees, what is the brain architecture and hyper-parameters, and what is its life expectancy and maturity age.
The DNA is inherited by from the creature ancestor/s in an evolutionary process.
The `DNA` class is defined in  [`evolution.py`](/evolution.py)

## DNA
The race defines a basic DNA to it's creatures. 
However, when each individual is born, the descendant does not get the same exact genes as his parents.
The mixing of two dna's is defined by in the method `Evolution.mutate_dna()` in [`evolution.py`](/evolution.py).
For asexual creatures, the dna of the mother cell is copied and some mutation are introduced.
For sexual races, the offspring dna is the mean gene value between the two parents plus a mutation.


## Fitrah
The ["Fitrah"](https://en.wikipedia.org/wiki/Fitra) is an Arabic word that has no exact English equivalent.
It is usually translated as “original disposition,” “natural constitution,” or “innate nature.”
The creature DNA includes a Fitrah part, which dictates his inherited tendency to perform a specific action.
The Fitrah is taken into account in addition to the brain decision, when selecting an action to take.
Note that the Fitrah is implemented simply as vector of action probabilities and do not take the current state into account.
Since the Fitrah is part of the creature dna, it cannot change during the lifetime of the creature, but is inherited to the creature descendants.
 