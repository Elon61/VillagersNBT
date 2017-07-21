from nbt import nbt
from matplotlib import pyplot

class Banana(object):
    id = 10


def srange(x1, xDoors, spaces):
    """
    a counting thing that i dunno what does.
    """
    for a in xrange(x1, x1 + xDoors):
        yield a
    for a in xrange(x1 + xDoors + spaces, x1 + spaces + xDoors * 2):
        yield a


def village_doors_coordinates(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis):
    """
    x1 and z1 are the lowest value on the X / Z axis
    'halfDoorsInVillage' is 1/2 of the total doors in a village
    :param axis: The axis along which a single village is created;

    make a MCEDIT filter to do the same thing could be cool,
    like a filter to create a village on every selected door, or on a row of doors on the X/Z axis.
    """

    k = []
    assert axis in ('X', 'Z')

    if axis == "Z":
        for x in xrange(x1, x1 + villages):
            j = [[x, y, z] for z in srange(z1, halfDoorsInVillage, emptySpaces)]
            k.append(j)
    elif axis == "X":
        for z in xrange(z1, z1 + villages):
            j = [[x, y, z] for x in srange(x1, halfDoorsInVillage, emptySpaces)]
            k.append(j)
    return k


number_of_villages_to_generate = 32
number_of_doors_to_generate = 22
tick = 77


def template_village_file(tick):
    """
    Creates a template villages.dat file that i can modify later on
    """
    cat = nbt.NBTFile()
    cat2 = cat['data'] = nbt.TAG_Compound()
    cat2["Villages"] = nbt.TAG_List(Banana)
    cat2['Tick'] = nbt.TAG_Int(tick)
    return cat


def existing_village_file(kovetz):
    """
    Create an editable villages.nbt file from an already existing one, using the same tick value
    """
    try:
        cat77 = nbt.NBTFile(kovetz)
    except IOError:
        raise Exception("Hmm. Unfortunately, the file requested does not exist :(")
    tick4 = cat77['data']['Tick'].value
    return cat77, tick4


class Village(object):
    """
    Some villages.dat related functions
    village is a tag_compound
    :type village: nbt.TAG_Compound
    """

    def __init__(self, village):
        self._village = village

    def add_door(self, door):
        """
        Adds a door and updates the current village aggregate and center with some magic math stuff
        """
        doors_list = self._village['Doors']
        doors_list.append(door)
        x = door['X'].value
        y = door['Y'].value
        z = door['Z'].value

        self._update_doormath(x, y, z)

    def del_doorz(self, new_doors):
        kapoow = self.doors_list()
        kapooww = list(kapoow)
        for door in kapooww:
            x, y, z = door['X'].value, door['Y'].value, door['Z'].value
            if (x, y, z) in new_doors:
                kapoow.remove(door)
                self._update_doormath(-x, -y, -z)

    def doors_list(self):
        return self.get_vil()['Doors']

    def list_doors(self):
        """
        LO TAYIM
        :return a set of tuples with the XYZ of all the doors in the village
        """
        doors_set = set()
        door_listcopy = list(self.get_vil()['Doors'])
        for door in door_listcopy:
            doors_set.add((door['X'].value, door['Y'].value, door['Z'].value))
        return doors_set

    def _update_doormath(self, x, y, z):
        doors_list = self._village['Doors']
        self._village['ACX'].value += x
        self._village['ACY'].value += y
        self._village['ACZ'].value += z
        if len(doors_list) == 0:
            self._village['CX'] = nbt.TAG_Int(0)
            self._village['CY'] = nbt.TAG_Int(0)
            self._village['CZ'] = nbt.TAG_Int(0)
        else:
            self._village['CX'].value = self._village['ACX'].value / len(doors_list)
            self._village['CY'].value = self._village['ACY'].value / len(doors_list)
            self._village['CZ'].value = self._village['ACZ'].value / len(doors_list)

    def del_door(self, x, y, z):
        """

        """
        door_taglist = self.get_vil()['Doors']
        door_listcopy = list(self.get_vil()['Doors'])
        for door in door_listcopy:
            if (door['X'].value, door['Y'].value, door['Z'].value) == (x, y, z):
                door_taglist.remove(door)
                self._update_doormath(-x, -y, -z)

    @property
    def is_empty(self):
        return len(self._village["Doors"]) == 0

    def get_vil(self):
        return self._village

    @staticmethod
    def create_village(tick):
        """
        Creates a template village
        """
        village_template = nbt.TAG_Compound()

        village_template['Doors'] = nbt.TAG_List(Banana)
        village_template['Players'] = nbt.TAG_List(Banana)
        village_template['ACX'] = nbt.TAG_Int(0)
        village_template['ACY'] = nbt.TAG_Int(0)
        village_template['ACZ'] = nbt.TAG_Int(0)

        village_template['CX'] = nbt.TAG_Int(0)
        village_template['CY'] = nbt.TAG_Int(0)
        village_template['CZ'] = nbt.TAG_Int(0)

        village_template['Golems'] = nbt.TAG_Int(0)
        village_template['MTick'] = nbt.TAG_Int(0)
        village_template['PopSize'] = nbt.TAG_Int(1)
        village_template['Radius'] = nbt.TAG_Int(32)
        village_template['Stable'] = nbt.TAG_Int(tick)
        village_template['Tick'] = nbt.TAG_Int(tick)
        return Village(village_template)


def create_door(tick, x, y, z):
    """
    Generates a door using given coords and tick.
    """
    door = nbt.TAG_Compound()
    door['TS'] = nbt.TAG_Int(tick)
    door['X'] = nbt.TAG_Int(x)
    door['Y'] = nbt.TAG_Int(y)
    door['Z'] = nbt.TAG_Int(z)
    return door


def del_door(vil_list, x, y, z):
    """
    Searches for a door with specified coordinates inside of specified village list,
    if the current village is out of doors, removes it.
    Can be used just to do some cleanup.
    """
    vil85 = list(vil_list)
    for vil_TAGCompound in vil85:
        villl = Village(vil_TAGCompound)
        villl.del_door(x, y, z)
        if villl.is_empty:
            vil_list.remove(vil_TAGCompound)

def all_coords_in_villages(cat):
    """
    LO TAYIM
    :param cat:
    :return:
    """
    doors_set = set()
    cat2 = cat['data']['Villages']
    vil17 = list(cat2)
    for village17 in vil17:
        vill = Village(village17)
        doors_set.update(vill.list_doors())
    return doors_set

def village_gen(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis, tick, cat):
    """
    generates villages with doors n stuff

    'x1' is the lowest block on the X axis
    'z1' is the lowest block on the Z axis
    'y'  is the Y level of the lower block of the doors
    :param axis: The axis along a single village is created;
    'axis' is the axis on which the villages are, either the axis where the in the village doors are,
    or the axis where the villages are, as in if i was to walk down that axis i would go through a door of every village

    'villages' is the numbers of villages i want on this layer
    'halfDoorsInVillage' is half of the doors in a village
    'emptySpaces' is the space between the 2 blocks of doors /
    the space between the first half of the doors and the second
    'tick' the time in ticks, in a new file can be basicly anything but 0 and in an old file it has the be the same as
    the other villages and the main tick of the file.
    'cat' magic NBT file

    """
    cat2 = cat["data"]
    doors_set = all_coords_in_villages(cat)
    doors_coords_lists = village_doors_coordinates(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis)
    for coordinates_list in doors_coords_lists:
        vil = Village.create_village(tick)
        for x, y, z in coordinates_list:
            if (x, y, z) in doors_set:
                del_door(cat2['Villages'], x, y, z)
            vil.add_door(create_door(tick, x, y, z))
            doors_set.add((x, y, z))
        cat2['Villages'].append(vil.get_vil())


def main():
    cat1, tick = existing_village_file("./villagesCopy.dat")
    bananana = Village(cat1['data']['Villages'][0])
    bananana.del_doorz(((1, 2, 3),))
    #village_gen(-107, number_of_villages_to_generate, 132, 169, number_of_doors_to_generate / 2, 19, 'X', tick, cat1)
    cat1.write_file("./villagesCopy.dat")

if __name__ == '__main__':
    main()