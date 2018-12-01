## Creatures

Creatures are intelligent agents that behave in the world. 
Their main goal is to survive and flourish.
Creatures have senses, basically vision, from which they get information about their local environment.

Each creature has a DNA which it inherits from his parents in an evolutionary process controlled in class evolution.
In the case of asexual creatures, the DNA is copied to the daughter cells.
The DNA define biological, intelligence, senses aspects of the creature.
For instance, how far it sees, what is the brain architecture and hyper-parameters, and what is its life expectancy and maturity age.

At each time step, the universe gives every creature a chance to make a single action.
To decide on his best action, the creature sees the environment around him and his internal states such as energy and age.
Using his brain he makes a decision and executes the action. 
The state description of the surrounding environment usually contains the location of food, creatures number and the total creature's energy in the space around him.
If it gets to the grid edge, the description of the out of grid cells will be marked by special number for each aspect.

Implementation wise, each race should be derived from  [`creature.py`](/creatures/creature.py).
It should implement some basic methods to define the race features.
For implementation examples, see class [`human.py`](/creatures/human.py), class [`bacterium.py`](/creatures/bacterium.py) and class [`zombie.py`](/creatures/zombie.py) taht inherits from class human but changes the action decision method.
### Races:
Every creature has a race. 
His race defines the actions he can make and whom he can make with and fight.
There could be several races in a single experiment.
Usually, the goal in such scenarios is to see which race is more effective and has better survival skills.
 

### Actions:
The actions implemented are the following: MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, EAT, MATE, DIVIDE and WORK.
Each creature has a subset of actions it can perform. 
These race abilities is specified in the class defining the race, which is derived from the creature class.
Not every action is possible in every situation, for instance, mating in not allowed before the creature get to maturity age.
Another example is that moving out of the grid is not possible in a non-slippery world.
If the creature tries to execute an implausible action, it loses a energy and his action will not take place.
Note that this loss of energy may lead to the creature dies.  


### Memory and Oral Tradition
The creature has a memory member that allow accumulating it's experiences.
The creature DNA limits the size of it's memory. 
"Oral Tradition" is the knowledge passed from generation to generation.
While this functionality is not implemented in the abstract class creature, in humans, a subclass of creature, ancestors inherit their memories to their offsprings.
Note that while the knowledge may pass between generations, the brain parameters are unique to each individual.


### DNA and Evolution
The race defines a basic DNA to it's creatures.
However, when each individual is born, the descendant does not get the same exact genes as his parents.
For asexual creatures, the dna of the mother cell is copied and some mutation are introduced.
For sexual races, the offspring dna is the mean gene value between the two parents plus a mutation.

   