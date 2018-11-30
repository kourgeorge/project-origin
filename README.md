
<div align="center">
  <img src="/docs/origin-icon.png"><br><br>
</div>

**project-origin** is the first attempt to create an artificial life environment that allows investigating how intelligence may be developed in different universes and under different rules.
It allows blending both Nature and Nurture, the two origins of intelligence, to build superior intelligence. 
See [Nature versus nurture](https://en.wikipedia.org/wiki/Nature_versus_nurture).
Researchers using project-origin can control and manipulate the physical environment, the biological rules and the learning mechanisms of the algorithm, and observe how different intelligence and behaviors can be developed under different rules.

The simulator is build of a [`Universe`](/docs/Universe.md) which is an environment that [`Creatures`](/docs/Creature.md) live in, adapt to, flourish or extinct.
The universe in project-origin has all aspects that any universe has like space, time, physics, evolution and chance.
Different universes may have different rules which we call *physics*. 
The [`Space`](/docs/Space.md) is a grid of 'Cells' that contain objects such as creatures, food, etc.
The creatures may have different senses and a different set of actions depending on the Race.
The most important aspect of the creature is its [`Brain`](/docs/Brain.md) which controls its actions given its internal and external state.
The universe reacts to the actions of the creatures under the laws of physics and biology.
Development and survival may be affected and controlled not only by the environment physics but also by the creature biological features, such as structure, sensors, and actions.

project-origin is made simple to allow fast training.
It has no graphics, however, it is built and visioned to be easy to imagine.
Most aspects of the simulator can be easily modified using inheritance and configuration files.

While still have no morphology and form, creatures have a brain, sensors and set of actions.
At each time step, they see their surrounding environment and select an action.
The creatures can move in the grid, eat, mate and fight.
Their destiny is controlled by the universe's physics, their genes and intelligence which dictates their actions, interactions and skills.




## Updates:
* 19.11.2018 - Added Artificial IQ tests to test the fit of creatures.
* 20.11.2018 - Added DQN based brain.
* 22.11.2018 - Adding Dashboard to visualize simulation progress.
* 23.11.2018 - Added App to allow dynamic control of simulation parameters.
* 24.11.2018 - Supporting Both human like creatures (WORK, MATE) and germs (EAT, DIVIDE, MOVE)
* 27.11.2018 - Supporting a 2-D Space and a better state representation + AIQ improvements
* 28.11.2018 - Tensor states (3D states) and Using Convnet in brain DQN. Defining Base Class for brain.
* 29.11.2018 - Supporting several creature races in the universe. Made new races creation easy.
* 30.11.2018 - Developing Gamified GUI to watch how different races compete and survive the battle.
* TBI - Different kinds of food and Dopamine implementation for DQN
