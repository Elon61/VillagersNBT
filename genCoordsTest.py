def testnameplsreplace(x1, x2, y, z1, z2):
    """
    make a MCEDIT filter to do the same thing could be cool,
    like a filter to create a village on every selected door, or on a row of doors on the X/Z axis.
    """
    k = []
    if x1 > x2:
        x1, x2 = x2, x1
    if z1 > z2:
        z1, z2 = z2, z1
    for x in xrange(x1, x2 + 1):
        for z in xrange(z1, z2 + 1):
            #k.append([x, y, z])
            k.extend([[x, y, z]])
    #k.append("end")
    #k.pop()
    return k

print testnameplsreplace(1, -10, 'Y', -1, 10)
