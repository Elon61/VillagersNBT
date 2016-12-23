#from ImportFile import *
from elonisapro.ImportFile import *

def srange(x1, xDoors, spaces):
    for a in xrange(x1, x1 + xDoors):
        yield a
    for a in xrange(x1 + xDoors + spaces, x1 + spaces + xDoors * 2):
        yield a


def testnameplsreplace(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis):
    """
    x1 and z1 are the lowest value on the X / Z axis
    'halfDoorsInVillage' is 1/2 of the total doors in a village
    Axis is The Villages Axis

    make a MCEDIT filter to do the same thing could be cool,
    like a filter to create a village on every selected door, or on a row of doors on the X/Z axis.
    """

    k = []
    assert axis in ('X', 'Z')

    if axis == "X":
        for x in xrange(x1, x1 + villages):
            j = [[x, y, z] for z in srange(z1, halfDoorsInVillage, emptySpaces)]
            k.append(j)
    elif axis == "Z":
        for z in xrange(z1, z1 + villages):
            j = [[x, y, z] for x in srange(x1, halfDoorsInVillage, emptySpaces)]
            k.append(j)
    return k

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(testnameplsreplace(1, 32, 'Y', 1, 11, 18, 'Z'))
#pp.pprint(testnameplsreplace(1, 11, 'Y', 1, 32, 18, 'X'))