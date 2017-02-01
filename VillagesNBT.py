from nbt import nbt
from genCoordsTest import testnameplsreplace
class Banana(object):
    id = 10

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
    cat77 = nbt.NBTFile(kovetz)
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

    def del_door(self, x, y, z):
        """

        """
        door_taglist = self.get_vil()['Doors']
        door_listcopy = list(self.get_vil()['Doors'])
        for door in door_listcopy:
            if (door['X'].value, door['Y'].value, door['Z'].value) == (x, y, z):
                door_taglist.remove(door)
                self._update_doormath(-x, -y, -z)

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

    def get_vil(self):
        return self._village


# def del_door(vil_list, x, y, z):
#     """
#     Searches for a door with specified coordinates inside of specified village list,
#     if the current village is out of doors, removes it.
#     Can be used just to do some cleanup.
#     """
#     for vil in vil_list:
#         vil2 = vil['Doors']
#         vil3 = list(vil['Doors'])
#         for door in vil3:
#             if (door['X'].value, door['Y'].value, door['Z'].value) == (x, y, z):
#                 vil2.remove(door)
#         if len(vil2) == 0:
#             vil_list.remove(vil)


def del_door(vil_list, x, y, z):
    """
    Searches for a door with specified coordinates inside of specified village list,
    if the current village is out of doors, removes it.
    Can be used just to do some cleanup.
    """
    #vil85 = list(vil_list)
    for vil_TAGCompound in vil_list:
        villl = Village(vil_TAGCompound)
        villl.del_door(x, y, z)
        if len(vil_TAGCompound["Doors"]) == 0:
            vil_list.remove(vil_TAGCompound)
    return vil_list

def create_village(tick):
    """
    Creates a template village
    """
    village = nbt.TAG_Compound()

    village['Doors'] = nbt.TAG_List(Banana)
    village['Players'] = nbt.TAG_List(Banana)
    village['ACX'] = nbt.TAG_Int(0)
    village['ACY'] = nbt.TAG_Int(0)
    village['ACZ'] = nbt.TAG_Int(0)

    village['CX'] = nbt.TAG_Int(0)
    village['CY'] = nbt.TAG_Int(0)
    village['CZ'] = nbt.TAG_Int(0)

    village['Golems'] = nbt.TAG_Int(0)
    village['MTick'] = nbt.TAG_Int(0)
    village['PopSize'] = nbt.TAG_Int(1)
    village['Radius'] = nbt.TAG_Int(32)
    village['Stable'] = nbt.TAG_Int(tick)
    village['Tick'] = nbt.TAG_Int(tick)
    return village

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

def village_gen(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis, tick, cat):
    """
    generates villages with doors n stuff

    'x1' is the lowest block on the X axis
    'z1' is the lowest block on the Z axis
    'y'  is the Y level of the lower block of the doors
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
    doors_coords_list = testnameplsreplace(x1, villages, y, z1, halfDoorsInVillage, emptySpaces, axis)
    for curr_vil in doors_coords_list:
        vil = Village(tick)
        for x, y, z in curr_vil:
            del_door(cat2['Villages'], x, y, z)
            vil.add_door(create_door(tick, x, y, z))
        cat2['Villages'].append(vil.get_vil())



#cat1, tick = existing_village_file("./villages.dat")
#village_gen(-669, number_of_villages_to_generate, 76, -221, number_of_doors_to_generate / 2, 19, 'Z', tick, cat1)
#cat1.write_file("./villagess.dat")

#cat959 = template_village_file(tick)
#cat960 = Village(create_village(tick))
#cat960.add_door(create_door(tick, 1, 20, 960))
#cat960.add_door(create_door(tick, 666, 666, 666))
#cat960.del_door(666, 666, 666)
#cat959["schnitzelim"] = cat960.get_vil()
#cat959.write_file("./villagesssss.dat")
cat34, tickss = existing_village_file("./villagesCopy.dat")
cat34['data']['Villages'] = del_door(cat34['data']['Villages'], 1, 3, 2)
cat34.write_file("./villagesCCopy.dat")

#TODO finish the del_door function and test it all
#TODO make this stuff a bit cleaner.
#TODO how about running it from cmd?
