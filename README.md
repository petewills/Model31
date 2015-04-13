# Model31

ROCK MODELLING
==============

This program models a set of reservoir layers, computing reflection timeshifts and amplitudes.
 - A "layer" is one rock unit, describer by a dictionary
 - A "stack" is a set of layers representing a 1D model
 - A "traverse" is a set of stacks, ordered, that represents a model along a line
 - A "vintage" is a traverse at one 4D time
 - A "survey" is a bunch of vintages, giving a 4D survey.

 It is written in plain python.


SETUP
=====

 1. Edit the "parameters" file. It is also python and is imported.
 2. "models.py" has example models that are called from main. Make one of these.


ABOUT THE CODE
==============

The code implements, mostly, the Gassmann equation.


CONTACT
=======
