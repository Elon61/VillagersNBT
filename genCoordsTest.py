import pprint
def testnameplsreplace(x1, xDoors, y, z1, zDoors, emptySpaces, Axis):
    """
    x1 and z1 are the lowest value on the X / Z axis
    xDoors is 1/2 of the total doors in a village
    Axis is The Villages Axis

    make a MCEDIT filter to do the same thing could be cool,
    like a filter to create a village on every selected door, or on a row of doors on the X/Z axis.
    """
    k = []
    j = []

    if Axis == "X":
        for x in xrange(x1, x1 + xDoors):
            for z in xrange(z1, z1 + zDoors):
                j.append([x, y, z])
            for z in xrange(z1 + zDoors + emptySpaces, z1 + emptySpaces + zDoors * 2):
                j.append([x, y, z])
            k.append(j)
            j = []
    elif Axis == "Z":
        for z in xrange(z1, z1 + zDoors):
            for x in xrange(x1, x1 + xDoors):
                j.append([x, y, z])
            for x in xrange(x1 + xDoors + emptySpaces, x1 + emptySpaces + xDoors * 2):
                j.append([x, y, z])
            k.append(j)
            j = []
    else:
        return
    return k

pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(testnameplsreplace(1, 32, 'Y', 1, 11, 18, 'X'))
pp.pprint(testnameplsreplace(-55, 11, 'Y', 1764, 32, 18, 'Z'))










#import pprint
#def testnameplsreplace(x1, x2, y, z1, z2, emptySpaces):
#    """
#    make a MCEDIT filter to do the same thing could be cool,
#    like a filter to create a village on every selected door, or on a row of doors on the X/Z axis.
#    """
#    k = []
#    j = []
#    if x1 > x2:
#        x1, x2 = x2, x1
#    if z1 > z2:
#        z1, z2 = z2, z1
#
#    for z in xrange(z1, z2 + 1):
#        for x in xrange(x1 + 1, x2 - emptySpaces + 1):
#            j.append([x, y, z])
#        for x in xrange(x1 + emptySpaces + 1, x2 + 1):
#            j.append([x, y, z])
#        k.append(j)
#        j = []
#
#    return k
#pp = pprint.PrettyPrinter(indent=2)
##print testnameplsreplace(0, 40, 'Y', 0, 32)
#pp.pprint(testnameplsreplace(0, 40, 'Y', 0, 32, 29))
#