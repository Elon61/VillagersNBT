from appJar import gui
from win32api import GetSystemMetrics
from matplotlib import pyplot
import VillagesNBT

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

NUM_VILLAGES = "Number of Villages:\t\t\t\t"
TOTAL_DOORS_PER_VILLAGE = "Total Doors in every village:\t\t\t"
SPACE_BETWEEN_DOORS = "Space between the 2 sets of doors:\t\t"
X_LOW = "Lowest X coordinate:\t\t"
Y = "First Y coordinate:\t\t\t"
Z_LOW = "Lowest Z coordinate:\t\t"

def plotplotplotplotplot(coordlist):
    """

    :param coordlist: weird coord list
    :return: cool stuff
    """
    colors = ["gs", "rs", "bs", "ys", "ms"]
    g = 0
    x = []
    z = []
    for i in coordlist:
        for j in i:
            pyplot.plot(j[0], j[2], colors[g % 5])
        g += 1


    pyplot.title("Villager points")

    nvillages = int(app.getEntry(NUM_VILLAGES))
    doorspervillage = int(app.getEntry(TOTAL_DOORS_PER_VILLAGE))
    doorsspace = int(app.getEntry(SPACE_BETWEEN_DOORS))
    x_low = int(app.getEntry(X_LOW))
    z_low = int(app.getEntry(Z_LOW))
    axis = app.getRadioButton("axis")

    if axis == "X":
        x_high = x_low + doorsspace + doorspervillage
        z_high = z_low + nvillages
    else:
        pass

    offset = 3

    pyplot.axis([x_low - offset, x_high + offset, z_low - offset, z_high + offset])
    pyplot.gca().set_autoscale_on(False)
    pyplot.show()

    return

def dirsel(name):
    print app.directoryBox("whatever")

def start(stuff):
    print app.getEntry(NUM_VILLAGES)
    return

def plot(schnitzel):
    nvillages = int(app.getEntry(NUM_VILLAGES))
    doorspervillage = int(app.getEntry(TOTAL_DOORS_PER_VILLAGE))
    doorsspace = int(app.getEntry(SPACE_BETWEEN_DOORS))
    x1 = int(app.getEntry(X_LOW))
    z1 = int(app.getEntry(Z_LOW))
    y = int(app.getSpinBox(Y))
    axis = app.getRadioButton("axis")
    print map(type, [nvillages, doorspervillage, doorsspace, x1, z1, y, axis])
    coords = VillagesNBT.village_doors_coordinates(x1, nvillages, y, z1, doorspervillage / 2, doorsspace, axis)
    plotplotplotplotplot(coords)
    return



app = gui("Test 1024")

app.setGeom("1280x720")
app.setLocation((width - 1280) / 2, (height - 720) / 2)
app.setResizable(False)
app.addLabelNumericEntry(NUM_VILLAGES, 0, 0, 3)
app.addLabelNumericEntry(TOTAL_DOORS_PER_VILLAGE, 1, 0, 3)
app.addLabelNumericEntry(SPACE_BETWEEN_DOORS, 2, 0, 3)
app.addLabelNumericEntry(X_LOW, 3, 0)
app.addLabelSpinBoxRange(Y, 1, 256, 3, 1)
app.addLabelNumericEntry(Z_LOW, 3, 2)
app.addMessage("InfoTextBox", "Startup complete! ", 7, 1, 3)
app.setMessageAlign("InfoTextBox", "left")

app.setEntry(NUM_VILLAGES, 64)
app.setEntry(TOTAL_DOORS_PER_VILLAGE, 22)
app.setEntry(SPACE_BETWEEN_DOORS, 19)
app.setEntry(X_LOW, 100)
app.setEntry(Z_LOW, 100)

app.addLabel("empty1", "\t\t\t", 0, 3)
app.addLabel("empty2", "\t\t\t\t\t\t", 0, 10)
app.setLabelBg("empty1", "red")
app.addButton("Folder Selection", dirsel, 0, 7, 1000)
app.addLabel("TextAxis", "Axis along which a single village is created:", 1, 7, 1000)
app.setLabelBg("TextAxis", "red")
app.addRadioButton("axis", "X", 3, 7, 1000)
app.addRadioButton("axis", "Z", 4, 7, 1000)
app.addButton("Start", start, 7, 7 , 100)
app.addButton("Simulate", plot, 6, 7 , 100)
#app.directoryBox("fileLoc")
app.setStretch("both")
app.go()
