<p align="center">
  <img src="https://github.com/kourgeorge/project-origin/blob/master/docs/origin-icon.png?raw=true"><br><br>
</p>

**project-origin** is an attempt to create an artificial life environment that allows studying intelligence development and evolution.
This area of study is known as [***Noogenesis***](https://en.wikipedia.org/wiki/Noogenesis).
Researchers using project-origin can observe how different behaviors can be developed under different nature rules, using both [Nature and Nurture](https://en.wikipedia.org/wiki/Nature_versus_nurture)
It gives a full control over the environment rules and mechanisms of learning to investigate tantalizing natural phenomena.

**project-origin** is a simulator that emulates a [`Universe`](/docs/Universe.md) in which [`Creatures`](/docs/Creature.md) live in, adapt to, flourish or extinct.
The universe has **Physics**, which dictates its nature, such as its Space, Time and Evolution.\\
The [`Space`](/docs/Space.md) is a grid of 'Cells' that contain objects such as creatures, food, etc.
[`Evolution`](/docs/Evolution.md) describe the content of the DNA and the rules of its creations and alternation.
Creatures are beings, defined by their **DNA**, which may have different senses and a different set of actions depending on their **Race**.
While still have no morphology and form, creatures have a [`Brain`](/docs/Brain.md), that defines their nature of intelligence and learning rules
Given information collected by the creature's senses about its surrounding environment, the brain selects an action.
Periodically, using its brain learning rules, the creature can improve its knowledge and optimize his actions. 
The main "goal" of the creatures is to increase their chance of survival under the environment physics, by learning to behave intelligibly and inherit their knowledge to their ancestors. 
Their destiny is determined by the universe's physics, their genes, skills, experience and intelligence.

project-origin is made simple and graphics-deficient to allow fast execution, however, it is built and visioned to be easy to imagine.
Most aspects of the simulator can be easily modified using programmatic inheritance and configuration files.

We believe that building a simulation which is close enough to reality, by modeling the important aspects of nature, could be a great method for practicing science.
In biology this this field is called [**"Artificial Life"**](https://en.wikipedia.org/wiki/Artificial_life).
We think that ***the understanding of a phenomena is substantially deeper, when the scientist not only can observe it, but can perceive the effect on it when changing the rules of nature.***
For more information about the scientific motivation visit [**this page**](/docs/Scientific.md).
In addition to the thrill of developing intelligent creators, project-origin allows you to observe the behavior and destiny of these creatures and maybe learn something about ourselves.

The current version of the project is the first seed, and several fundamental features are planned for future releases.
See [**the Future Plans page**](/docs/FuturePlans.md) for more information.

_We are more than happy to hear your comments, idea, and contribution.
Please contact us in the following address "kourgeorge at gmail dot com", or simply open an issue._

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
