# treegen.py
#
# Random tree-generation with density option
import random
from pymclevel import MCSchematic

# Use the inputs variable to tell MCEdit we want a Density option. See filterdemo.py for more info.
inputs = (
    ("Axis", ("X", "Z")),  # Integer input, default: 10, min: 1, max: 100.
)


# The perform function is where we receive a reference to the level object, a BoundingBox object for the current selection, and an options dict holding the options the user specified.

def perform(level, box, options):
    pass