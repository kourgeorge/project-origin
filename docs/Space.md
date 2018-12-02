## Space
The [`space`](/space.py) is built up of a matrix of [`Cells`](/cell.py).
Depending on the configuration, each Cell can contain a limited or unlimited number of creatures and the food.

The universe is not exposed directly to Cells but uses space as a proxy.
Thus, most of the services the class space provides are delegated to the Cell class.
However, it provides additional services such as returning the state in a given coordinate and finding another creature, for mating, fighting, etc.

Depending on the configuration, space may be slippery or edged.
If space is edged, creatures which get to the edge of the grid, and choose to take a step out of it, will stay in place.
They are not encouraged to do so, because they will pay in MOVE energy but stay in place.
If space is slippery, doing so will cause the creature to fall from the grid and die.
