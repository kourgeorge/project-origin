## Motivation

When thinking about Artificial Intelligence (AI) what most people in the field have in mind is machine learning models and 
heuristics to solve problems that are complex enough that their solution cannot be written using an exact set of steps but 
should be learned from data or from interaction with the environment.
In this narrow view, AI is a collection of procedures that can be seen as a smart extension of functions (in classical computer programs) that we can employ to make our life easier.
However, contemplating the term "artificial intelligence" in my view means much more. 
It may refer to Intelligent creatures or subjects that live in some universe and want to survive using their intelligence and skills.
Depending on the universe rules and physics they live in, these creatures may develop complicated skills such as collaboration and communication.

In the last few years, with the emerging interest in deep learning and reinforcement learning, there has been a great effort to develop environments
that can be used to demonstrate the ability of AI.
Nevertheless, most of these simulations are game environment, see for instance, OpenAI gym [https://gym.openai.com/], deepmind lab [https://github.com/deepmind/lab], OpenAI Universe [https://blog.openai.com/universe/].
However, the limitation of game environments is that the actions of the agents are limited and its goal is too strict.
While it is nice to show how artificial agent can master games, it is more interesting to see  how artificial creatures can develop
complex behavior, social behavior, and survival skills.

**Can we create intelligent creatures that can develop survival skills such as collaboration and communication?**
Namely, being put in a challenging environment, can the state of the art AI, using trial and error and evolution, 
learn how to survive?
Can it figure out complex behavior, from the procedural and social viewpoints, if that is required to their survival?  
Would they learn using their actions (moving, mating, fighting and producing sound) to flourish?
Would they "understand" the effect of these actions on their own survival and on the environment? 
Would they develop non-obvious behavior showing their understanding of the effect of time and age?
How fast can they adapt to changes in the environment that change the game rule like epidemic or dearth?  


## The Story of Project Origin

Progect Origin is the first attempt to develop an environment that allows investigating how intelligence may be developed under a specific physics.
How it can learn to survive and react to signals from the environment using reinforcement learning.
An algorithm (a model) can develop such skills in the same way algorithm learn to play Atari 2600 games. 

*Universes* are environments that *creatures* live in, adapt to, flourish or extinct.
Different universes may have different rules which we call *physics*. 
The creatures may have different senses and a different set of actions.
The most important aspect of the creature is its brain which controls its actions given its internal and external state.
It is interesting to see how different intelligence and behaviors can be developed under different physics.
Intelligence may be affected and controlled not only by the environment physics but also by the creature physical structure, sensors, and actions.

Project Origin simulator is made simple to allow fast training.
It has no graphics, however, it is built and visioned to be easy to imagine.
Origin has all the aspect that any universe has: Space, time, physics and chance.
Space is called the *Grid* and is implemented as a matrix of *Cells*.
Each cell can contain objects such as creatures, food, etc.
The physics (rules), time and chance are controlled by the universe. The universe also reacts to the actions of the creatures under the laws of physics. 

The creatures in origin called "Mangos", viz. "Mango" is the name of their race.
Mangos may have private names which must have the "mango" prefix. 
For instance, "Mangolid", "Mangodo" and "Mangodino" are all valid names for mangos.

While still have no morphology and form, mangos have a brain, sensors and set of actions.
At each time step, they see their surrounding environment and select an action.
The creatures can move in the grid, eat, mate and fight.
Their destiny is controlled by the universe's physics, but mainly by their intelligence which dictates their actions, interactions and skills.

In addition to the thrill of developing intelligent creators, origin allows you to observe the behavior and destiny of these creatures and maybe learn something about ourselves.


Answering these questions, by demonstrating how complicated skills can be developed by artificial agents in a simulation
would shed some light and take us closer toward understanding the mechanics and the true nature of our intelligence.
It may even reveal some insights about more abstract nature and skills that animal and humans possess, like socializing, communication and even love. 

To make these ideas more tangible consider the following examples: 
- Assume that the physics of the simulation dictates that two creatures should be in specific place and perform 
a specific operation simultaneously in order to both get reward, would they learn to do so?
- If doing an action in a specific age or a specific time cycle of the universe, could result in a great reward, would make them "wait" to this age to do the action?

### The future of Project Origin
This project is a seed for a far-reaching vision. In the future, it should allow developing a wide variety of universes. Below are some examples of future capabilities of project Origin:

- Project Origin should allow extending the physics of the environment easily and maybe incorporate realistic physical simulators.
- It should support morphology of creatures, i.e. to give physical shape to creatures, that may affect their capabilities such as movement speed, power, etc.
- It should support the introduction of different objects with a variety of functionalities and behavior to the universe.
- While currently, space is a 1-D, in the future it should allow supporting different types of spaces.
- Controlling biological aspects of physics such as mating rule, evolution, and intelligence inheritance.
- It should allow extending the creature's capabilities, such as adding vocal communication and even love, hate, and motivation.
- It should allow defining dynamic natures, like periods of dearth and epidemics. 
- Online visualization of the population and environment statistics such as creatures locations actions distribution and food location.
- Online control of nature to observe the effect of the population. 
- Use dynamic graph deep learning framework such as TensorFlow 2.0 or Pytorch