## Creatures

Creatures are intelligent agents that live and behave in the universe. 
Their main goal is to survive and flourish.
Creatures have senses, basically vision, from which they get information about their local environment.
Different creatures may have a different set of abilities, namely, different actions they can do in their environment and to other surrounding creatures.

Creatures belong to a **Race** (see below) determined by the race of his ancestors and which define his set of abilities (actions).  
It has a DNA which it inherits from his parents in an evolutionary process controlled by the evolution.
See more information in [Evolution.md](/docs/Evolution.md).
At each time step, the creature makes an action, which is decided upon by one or several "intelligence sources" such as his brain, his instincts and by chance.
To decide on his best action, the creature sees the environment around him and his internal states such as energy and age. 
In reinforcement learning terminology, this is called the "environment state".
The state description of the surrounding environment may contain the distribution of food, creatures, their race, and energy.
If the edge of the grid is in the vision range of the creature, each aspect of the environment in the location of the edge and beyond will be marked by (-1).

### Races:
The creature race defines the actions he can make and whom he can mate with and fight.
There could be several races in a single experiment.
Usually, the goal in such scenarios is to see which race is more effective and has better survival skills. 


### Memory and Oral Tradition
The creature has a memory that accumulates its experiences.
The size of the memory is limited by the creature's DNA. 
"Oral Tradition" is the knowledge passed from generation to generation.
While this functionality is not implemented in the abstract class creature, in humans, a subclass of creature, ancestors inherit their memories to their offsprings.
Note that while the knowledge may pass between generations, the brain parameters are unique to each individual.


### Creating New Creatures
Implementation wise, each race should be derived from  [`abstractcreature.py`](/creatures/abstractcreature.py) or from one of its sub-classes.
It should implement some basic methods to define the race nature.
For implementation examples, see class [`human.py`](/creatures/human.py), class [`bacterium.py`](/creatures/bacterium.py) and class [`zombie.py`](/creatures/zombie.py) that inherits from class human but changes the action decision method.
One of the important methods in the creature is the `decide` method, which given the state, decides on an action.
It may take into consideration the brain recommendation, the fitrah, the creature curiosity mechanism, age, energy or any other information to make a decision.
