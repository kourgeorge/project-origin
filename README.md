<p align="center">
  <img src="https://github.com/kourgeorge/project-origin/blob/master/docs/origin-icon.png?raw=true"><br><br>
</p>

[![DOI](https://zenodo.org/badge/141611333.svg)](https://zenodo.org/badge/latestdoi/141611333)

**project-origin** is an attempt to create an artificial life environment that allows studying intelligence emergence and evolution.
An area of study which is known as [***Noogenesis***](https://en.wikipedia.org/wiki/Noogenesis).
project-origin allows researchers to simulate different nature rules and mechanisms of learning that enable the development of a wide variety of behaviors determined by intelligence governed by both [Nature and Nurture](https://en.wikipedia.org/wiki/Nature_versus_nurture).
In addition to the thrill of developing a new type of artificial intelligence, project-origin allows its users to investigate tantalizing natural phenomena by observing the behavior and destiny of intelligent creatures.
For more information about the scientific motivation behind project-origin visit [**this page**](/docs/Scientific.md).

project-origin is a simulator that emulates a [`Universe`](/docs/Universe.md) in which [`Creatures`](/docs/Creature.md) live in, adapt to, flourish or extinct.
The universe has **Physics**, which are basic rules dictating its nature, such as it's **Space**, **Time** and **Evolution**.
The [`Space`](/docs/Space.md) is basically a grid of 'cells' that inhibits objects such as creatures, food, etc.
The [`Evolution`](/docs/Evolution.md) in project-origin describes the content of the creatures DNA and the rules of its creations and alternation.
Creatures are beings, defined by their **DNA**, which may have different senses and a different set of actions depending on their **Race**.
While still have no morphology and form, creatures have a [`Brain`](/docs/Brain.md), that defines the nature of their intelligence.
The brain role is to select an action given information about the creature's surrounding environment and its internal state.
Periodically, using its brain learning rules, the creature can improve its knowledge and optimize his actions. 
The actions of the creature are not determined solely by the brain but also affected by the creature inherited [**Fitrah**](https://en.wikipedia.org/wiki/Fitra).
The main "goal" of the creatures is to increase their chance of survival under the environment physics, by learning to behave intelligibly.
While the intelligence of the creature is determined by its genes and brain, there are three mechanisms for collecting knowledge.
1. Evolution and inheritance (including the fitrah), (2) experience (trial and error) and (3) "Oral Tradition" representing part of the ancestors' knowledge.  
Their destiny is determined by the universe's physics, their genes, skills, experience, and intelligence.

We believe that building a simulation which is close enough to reality, by modeling the important aspects of nature, could be a great method for practicing science.
In biology, this field is called [**"Artificial Life"**](https://en.wikipedia.org/wiki/Artificial_life).
We think that _the understanding of a phenomenon is substantially deeper when not only it can be observed in a fixed environment, but its nature is perceived in different settings._

project-origin is made simple and graphics-deficient to allow fast execution, however, it is built and visioned to be easy to imagine.
Most aspects of the simulator can be easily modified using programmatic inheritance and configuration files.
The current version of the project is the first seed, and several fundamental features are planned for future releases.
See [**the Future Plans page**](/docs/FuturePlans.md) for more information.

_We are more than happy to hear your comments, ideas, and contribution.
Please contact us in the following address "kourgeorge at gmail dot com", or simply open an issue._

### Citing project-origin
```
@misc{kour2018projectorigin,
  author       = {Kour, George},
  title        = {project-origin: an artificial life simulator for investigating noogenesis},
  month        = December,
  year         = 2018,
  doi          = {10.5281/zenodo.8475},
  howpublished = {\url{https://kourgeorge.github.io/project-origin/}}
}
```

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
