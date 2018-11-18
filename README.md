## Introduction

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

## Scientific Motivation
Project Origin can be employed to get us closer to answering intriguing questions on **intelligence**, on the **behavior of intelligent creatures** and maybe help us **hypothesise on the reason underlying nature rules**.

In the intelligence realm, first, it is a realistic environment for training intelligent creatures with various skills.
Second, it may provide us with a depper understanding of the development of complex skills from basic actions.
Third, it can show us how intelligence and evolution, are two different mechanisms that affect each other and "cooperate" to build intelligence.

Below are several example questions embodying these aspects:
 - Can we create intelligent creatures that can develop survival skills such as collaboration and communication?
Namely, being put in a challenging environment, can the state of the art AI, using trial and error and evolution, 
learn how to survive?
- Can they learn to look for food?
- Can it figure out complex behavior, from the procedural and social viewpoints, if that is required to their survival?  
- Would they learn using their actions (moving, mating, fighting and producing sound) to flourish?
- Would they "understand" the effect of these actions on their own survival and on the environment? 
- Would they develop non-obvious behavior showing their understanding of the effect of time and age?
- How fast can they adapt to changes in the environment that change the game rule like epidemic or dearth?  

In addition, this project can be used as a tool by researchers in different disciples of science to give possible explanations to a wide range of phenomena in nature and help us reveal the essentiality of specific rules.
For instance, consider the question of the need for minimal reproduction age in organisms biology.
One answer may be that this mechanism ensures that anscestors are physically and mentally mature enough to be able to take care of their offsprings. 
However, this is an insufficient explanation when it comes to germs or other organisms that do not take care of their offsprings but their biolology implements this mechanism.
Using the simulation we noted that if no maturity age is implemented in the universe, a population explosion consisting of stupid creatures may happen.
This statistically can happen because natural selection can push them to reproduce frequently and immediately after birth, allowing their race to flourish without showing any tracts of intelligent behavior.
However, this phenomenon rarely happens in universes enforcing maturity age.
This suggests that the minimal reproduction age is implemented in nature not only to make sure that anscestors are mature enough to be able to take care of their offsprings but also that the maturity age is an essential element of the developing intelligent and fit creatures. Namely, one should prove that it has some survival abilities before passing down its genes.
This is a nice example showing how natural selection and intelligence are basically two mechanisms that work together to produce fit creatures.

Talking with Dr. Joseph Fanous (a.k.a *"iljoe"*) - a pharmaceutical scientist and a close friend of mine; he mentioned that such simulation, not only can help giving alternative an interesting answers to long standing questions in biology but can be used to also to answer questions raised by recent observations about the behaviour of organisms. 
For instance in his field of study - bacterial sciences and antibiotics development, such simulation can help giving answers about the underlying mechanisms of bacterial developments including:
- Why germs which develope more slowely show better survivals skills?
- How persistors develope? persistors are germ individuals that develope superior survival abilitites in a hostile environment (e.g., an environment with antibiotics).
- Explain why pathogens behave differently in lab bacterial culture vs. in organismic hosts? How they learn to use different aspects of the environment to survive when they are in environments with different hostile agents. For instance, in lab bacterial culture the germs mostly eat the glucose provided in the Petric plate but in the organic host, they eat feces of their friends.

Building a simulation which is close enough to reality by modeling the important aspects of nature could be a great tool and a new method for practicing science. 
***Once the experimenter is not only explaining by observing a phenomenon under specific physics but can play "god" and change the rules of nature and observe the effect of the change on the phenomenon, he can obtain a deeper understanding of nature. ***

## The Story of Project Origin

Project Origin is the first attempt to develop an environment that allows investigating how intelligence may be developed under a specific physics.
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

## Widening the horizons of Intelligence research
In the current implementation of Project Origin, there are aspects that in other game environment is not possible or not relevant, for instance, the combination of Evolution and Learning for development and survival in the race.
In the current implementation of Origin DNA can affect some biological aspects of the creature, for example, changing its sight range.
While all implementations of agents playing games, has a constant input state size, in Origin different policy graphs can be implemented with a different number of input parameters or even different inner structure of state input or action set output and parameters.
In addition, the neural network train and improve using backpropagation during the lifetime of the creature.
This allows investigating how both evolution and intelligence contribute to the creation of highly skilled creatures.

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
