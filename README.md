<p align="center">
  <img src="https://github.com/kourgeorge/project-origin/blob/master/docs/origin-icon.png?raw=true"><br><br>
</p>

**project-origin** is an attempt to create an artificial life environment that allows studying intelligence development and evolution.
This area of study is known as [***Noogenesis***](https://en.wikipedia.org/wiki/Noogenesis), which means the emergence and evolution of intelligence.

It allows blending both [Nature and Nurture](https://en.wikipedia.org/wiki/Nature_versus_nurture), the main two origins of intelligence, to build superior intelligence. 
Researchers using project-origin can observe how different intelligence and behaviors can be developed under different physical and biological universes.
It gives a full control over the environment rules and mechanisms of learning to investigate the phenomenon of noogenesis.

**project-origin** is basically a simulator that emulates a [`Universe`](/docs/Universe.md) which is an environment that [`Creatures`](/docs/Creature.md) live in, adapt to, flourish or extinct.
The universe in project-origin, as like any other universe has **Physics** which contains the rules of Space, Time, Evolution and Learning.
The [`Space`](/docs/Space.md) is a grid of 'Cells' that contain objects such as creatures, food, etc.
[`Evolution`](/docs/Evolution.md) describe the content of the DNA and the rules of its creations and alternation.
Creatures are beings, defined by the **DNA**, may have different senses and a different set of actions depending on their **Race**.
While still have no morphology and form, creatures have a [`Brain`](/docs/Brain.md), that defines their nature of intelligence and learning rules
Given information collected by the creature's sensors about its surrounding environment, the brain selects an action and using learning rules, learns how to act optimally. 
The main "goal" of these creatures is to increase their chance of survival under the environment physics, by learning to behave intelligibly and pass their knowledge to their ancestors. 
Their destiny is controlled by the universe's physics, their genes which dictates their actions, interactions, and intelligence.

project-origin is made simple to allow fast training.
It has no graphics, however, it is built and visioned to be easy to imagine.
Most aspects of the simulator, can be easily modified using inheritance and configuration files.
Building a simulation which is close enough to reality, by modeling the important aspects of nature, could be a great tool and a new method for practicing science, especially in biology, in which this field is called [**"Artificial Life"**](https://en.wikipedia.org/wiki/Artificial_life).
***Once the experimenter is not only observing a phenomenon under specific physics but can change the rules of nature and observe the effect of the change on the phenomenon, his understanding of the phenomenon deepens.***
For more information about the scientific motivation visit [**this page**](/docs/Scientific.md).

The current version of the project is the first seed, and several fundamental features are planned for future releases.
See [**the Future Plans page**](/docs/FuturePlans.md) for more information.

_We are more than happy to hear your comments, idea, and contribution.
Please contact us in the following address "kourgeorge at gmail dot com", or open an issue._

### Updates:
* 19.11.2018 - Added Artificial IQ tests to test the fit of creatures.
* 20.11.2018 - Added DQN based brain.
* 22.11.2018 - Adding Dashboard to visualize simulation progress.
* 23.11.2018 - Added App to allow dynamic control of simulation parameters.
* 24.11.2018 - Supporting Both human like creatures (WORK, MATE) and germs (EAT, DIVIDE, MOVE)
* 27.11.2018 - Supporting a 2-D Space and a better state representation + AIQ improvements
* 28.11.2018 - Tensor states (3D states) and Using Convnet in brain DQN. Defining Base Class for brain.
* 29.11.2018 - Supporting several creature races in the universe. Made new races creation easy.
* 30.11.2018 - Developing Gamified GUI to watch how different races compete and survive the battle.
* 30.11.2018 - Oral tradition implementation - supporting inheriting experience to descendants.
* 01.12.2018 - Adding the Fitrah to the DNA- an expression of the innate nature of a creature. Improving the state representation.
* TBI - adding Dopamine implementation for RL algorithms.
