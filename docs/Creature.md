## Creatures

Creatures are intelligent agents that behave in the world. 
Their main goal is to survive and flourish.
Creatures have senses, basically vision, from which they get information about their local environment.

Each creature has a DNA which it inherits from his parents in an evolutionary process controlled in class evolution.
In the case of diving creatures, the DNA is copied to the daughter cells.
The DNA define biological, intelligence, senses aspects of the creature.
For instance, how far it sees, what is the brain architecture and hyper-parameters, and what is its life expectancy and maturity age.

At each time step, the universe gives every creature a chance to make a single action.
To decide on his best action, the creature sees the environment around him and his internal state such as energy and age.
Using his brain he makes a decision and executes the action. 
The state description of the surrounding environment usually contains the location of food, creatures number and the total creatures energy in the space around him.
If it gets to the grid edge, the description of the out of grid cells will be marked by special number for each aspect.

Every creatures has race. His race define the actions he can make and whom he can make with and fight.
There could me several races in a single experiment.
Usually the goal in such scenarios is to see which race is more effective and has better survival skills.


### Actions:
The actions implemented are the following: MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, EAT, MATE, DIVIDE and WORK.
Each creature has a subset of actions it can perform. 
Not every action is possible in every situation, for instance, mating in not allowed before the creature get to maturity age.
Another example is that moving out of the grid is not possible in a non-slippery world.
If the creature tries to execute a not plausible actions, it looses a energy equals to the MOVE energy and his action will not take place.
Note that this lose of energy may lead to the creature death.  

The race abilities should be specified in the class defining the race, which is derived from the creature class.

