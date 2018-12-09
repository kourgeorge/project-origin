## Simulation Installation and Execution:

Currently, the project can run in two modes, with or without GUI.
The GUI is basically a dashboard that provides aggregated information about the population state, location, actions, age, AIQ, etc..

First you should install all requirements using the following command:\
`pip3 install -r requirements.txt` \

if you are using Anaconda use the following:\
`conda install --yes --file requirements.txt`

To run GUI, run the following command:\
`python app.py`

To run the simulator in console mode use the following command:\
`python simulator.py`

## Changing the simulator configuration
To select the creatures to put in the universe, use the simulation configuration file, [`configsimulator.py`](configsimulator.py).
in the config file you can play with the physical and biological configuration of the environment. see [`config.py`](config.py).

## Dev mode:
Auto generate requirement file:\
`pipreqs origin --force`