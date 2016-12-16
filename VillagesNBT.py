from nbt import nbt
class banana(object):
    id = 10

number_of_villages_to_generate = 8
number_of_doors_to_generate = 16
tick = 77

cat = nbt.NBTFile()
cat2 = cat['data'] = nbt.TAG_Compound()

cat2['Villages'] = nbt.TAG_List(banana)
cat2['Tick'] = nbt.TAG_Int(tick)

village_list = cat2['Villages']
class Village(object):
    """
    Village in minceraft
    """
    def __init__(self, tick):
        self._village = create_village(tick)

    def add_door(self, door):
        doors_list = self._village['Doors']
        doors_list.append(door)

        self._village['ACX'] = nbt.TAG_Int(door['X'].value + self._village['ACX'].value)
        self._village['ACY'] = nbt.TAG_Int(door['Y'].value + self._village['ACY'].value)
        self._village['ACZ'] = nbt.TAG_Int(door['Z'].value + self._village['ACZ'].value)

        self._village['CX'] = nbt.TAG_Int(self._village['ACX'].value / len(doors_list))
        self._village['CY'] = nbt.TAG_Int(self._village['ACY'].value / len(doors_list))
        self._village['CZ'] = nbt.TAG_Int(self._village['ACZ'].value / len(doors_list))

    def get_vil(self):
        return self._village

def create_village(tick):
    """
    """
    village = nbt.TAG_Compound()

    village['Doors'] = nbt.TAG_List(banana)
    village['Players'] = nbt.TAG_List(banana)
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
    door = nbt.TAG_Compound()
    door['TS'] = nbt.TAG_Int(tick)
    door['X'] = nbt.TAG_Int(x)
    door['Y'] = nbt.TAG_Int(y)
    door['Z'] = nbt.TAG_Int(z)
    return door

'''
if True:
    del village_list[:]
    village_list.append(nbt.TAG_Compound())
    current_V_dict = village_list[-1]
    current_V_dict['Doors'] = nbt.TAG_List(banana)
    current_V_dict['Players'] = nbt.TAG_List(banana)
    current_V_dict['ACX'] = nbt.TAG_Int(0)
    current_V_dict['ACY'] = nbt.TAG_Int(64)
    current_V_dict['ACZ'] = nbt.TAG_Int(4)

    current_V_dict['CX'] = nbt.TAG_Int(0)
    current_V_dict['CY'] = nbt.TAG_Int(64)
    current_V_dict['CZ'] = nbt.TAG_Int(4)

    current_V_dict['Golems'] = nbt.TAG_Int(0)
    current_V_dict['MTick'] = nbt.TAG_Int(0)
    current_V_dict['PopSize'] = nbt.TAG_Int(1)
    current_V_dict['Radius'] = nbt.TAG_Int(32)
    current_V_dict['Stable'] = nbt.TAG_Int(1)
    current_V_dict['Tick'] = nbt.TAG_Int(1)


    doors_list = current_V_dict['Doors']
    del doors_list[:]
    doors_list.append(nbt.TAG_Compound())
    new_door_dict = doors_list[-1]

    new_door_dict['TS'] = nbt.TAG_Int(1)
    new_door_dict['X'] = nbt.TAG_Int(0)
    new_door_dict['Y'] = nbt.TAG_Int(64)
    new_door_dict['Z'] = nbt.TAG_Int(4)
'''

#village_list.append(create_village(tick))
#doors_list = village_list[0]['Doors']
#doors_list.append(create_door(77, 88, 99, 11))

for i in xrange(number_of_villages_to_generate):
    vil = Village(tick)
    for l in xrange(number_of_doors_to_generate):
        vil.add_door(create_door(tick, 1, 2, 4))
    cat2['Villages'].append(vil.get_vil())
cat.write_file("./cat.dat")

#TODO Add a thing that makes it that when adding a door it will check for any door with the same coordinates in any village and remove it from any village that isnt from the ones created
#TODO read the tick of the file and apply it to all the new villages