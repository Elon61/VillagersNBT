from PIL import Image
from appJar import gui
from win32api import GetSystemMetrics
from matplotlib import pyplot
import os
import shutil
import VillagesNBT
import errno
import glob, time
import hotshot, hotshot.stats
import threading

width = GetSystemMetrics(0)
height = GetSystemMetrics(1)

currFolder = r"C:\Users\Elon\Desktop\Stuff"

NUM_VILLAGES = "Number of Villages:\t\t\t\t"
TOTAL_DOORS_PER_VILLAGE = "Total Doors in every village:\t\t\t"
SPACE_BETWEEN_DOORS = "Space between the 2 sets of doors:\t\t"
X_LOW = "Low X coordinate:\t\t"
Y = "Y coordinate:\t\t\t"
Z_LOW = "Low Z coordinate:\t\t"

bananaprofiler = hotshot.Profile("banana.prof")
bananaprofiler.start()

def bakefile(fileloc):
    """
    assumes directory exists; bad
    :param fileloc:
    :return:
    """
    if os.path.isfile(fileloc + ".bak_latest"):  # maybe add date to name.
        for i in xrange(1, 9):
            #do stuff i guess, make the latest.. hmm.. smth? and then create a new latest i guess.
            if os.path.isfile(fileloc + ".bak_" + str(i)):
                pass
            elif i == 8:
                #if '/' in fileloc:
                #    folder = '/'.join(fileloc.split('/')[:-1])
                #elif '\\' in fileloc:
                #    folder = '\\'.join(fileloc.split('\\')[:-1])
                #app.infoBox("PLZ BUY PREMIUM TO CONTINUE", "Backup limit reached: overwriting oldest backup")
                folder = os.path.dirname(fileloc)
                oldestbak = min(glob.iglob(folder + r"\*.dat.bak_?"), key=os.path.getmtime)
                shutil.copy(fileloc + ".bak_latest", oldestbak)
                shutil.copy(fileloc, fileloc + ".bak_latest")
                break
            else:
                shutil.copy(fileloc + ".bak_latest", fileloc + ".bak_" + str(i))
                #turns latest backup into (number)
                shutil.copy(fileloc, fileloc + ".bak_latest")
                #take the villagers.dat and backups it into bak_latest
                break
    else:
        shutil.copy(fileloc, fileloc + ".bak_latest")
    pass

def cleanup():
    try:
        os.remove("template.png")
    except OSError:
        pass
    try:
        os.remove("plot.jpg")
        os.remove("plot.gif")
    except OSError:
        pass

    pass

def plotplotplotplotplot(coordlist):
    """

    :param coordlist: weird coord list
    :return: cool stuff
    """
    colors = ["gs", "rs", "bs", "ys", "ms"]
    g = 0
    for vilpoints in coordlist:
        for doorloc in vilpoints:
            pyplot.plot(doorloc[0], doorloc[2], colors[g % 5])
        g += 1

    pyplot.title("Villager points")

    x_low = min([i[0] for x in coordlist for i in x])
    z_low = min([i[2] for x in coordlist for i in x])
    x_high = max([i[0] for x in coordlist for i in x])
    z_high = max([i[2] for x in coordlist for i in x])

    offset = 3
    pyplot.xlabel("X axis")
    pyplot.ylabel("Z axis")
    pyplot.axis([x_low - offset, x_high + offset, z_low - offset, z_high + offset])
    pyplot.gca().set_autoscale_on(False)
    pyplot.savefig("plot.jpg")

    width1, height1 = Image.open("plot.jpg").size

    Image.open("plot.jpg").save("plot.gif")

    app.openSubWindow("simimg")
    app.setImage("simimg", "plot.gif")
    app.setImageSize("simimg", width1, height1)
    app.stopSubWindow()
    app.showSubWindow("simimg")
    return

def startthread(banana):
    threading.Thread(target=start).start()

def start():
    if app.getRadioButton("backup") == "Yes":
        app.setLabel("Info", "Baking old village file.")
        time.sleep(.5)
        try:
            bakefile(currFolder + r"\villages.dat")
            app.setLabel("Info", "Old villages file baked!")
        except IOError, e:
            if e.errno == errno.ENOENT:
                pass
            else:
                app.setLabel("Info", "IOError " + str(e.errno) + ": " + str(e.strerror))


    num_of_villages_to_generate = int(app.getEntry(NUM_VILLAGES))
    total_doors_per_village = int(app.getEntry(TOTAL_DOORS_PER_VILLAGE))
    doorspace = int(app.getEntry(SPACE_BETWEEN_DOORS))
    x = int(app.getEntry(X_LOW))
    y_list = app.getAllListItems("Y list")
    z = int(app.getEntry(Z_LOW))
    axis = app.getRadioButton("axis")

    y_list = map(int, y_list)

    if not y_list:
        app.setLabel("Info", "No Y coord selected, please select stuff")
        return

    if os.path.exists(currFolder + "/villages.dat"):
        vilFile, tick = VillagesNBT.existing_village_file(currFolder + "/villages.dat")
        app.setLabel("Info", "Village file found!")
        time.sleep(1)
    else:
        tick = 0
        vilFile = VillagesNBT.template_village_file(tick)
        vilFile.write_file(currFolder + "/villages.dat")
        app.setLabel("Info", "No file found: creating new file.")
        time.sleep(1)

    app.setLabel("Info", "Creating Villages, might take a while, be patient!")
    print y_list
    VillagesNBT.village_gen(x, num_of_villages_to_generate, y_list, z,
                                total_doors_per_village / 2, doorspace, axis, tick, vilFile)

    try:
        vilFile.write_file(currFolder + "/villages.dat")
        app.setLabel("Info", "Success!")
    except IOError, e:
        if e.errno == errno.EACCES:
            app.setLabel("Info", "Permission denied ;(")
            raise Exception("Hmmm, Permission denied ;(")
        else:
            app.setLabel("Info", "IOError " + str(e.errno) + ": " + str(e.strerror))
            raise

    return

def add_y(stuff):
    y = app.getSpinBox(Y)
    currYval = int(app.getSpinBox(Y))
    app.addListItem("Y list", y)
    app.setLabel("Info", "Y value \'" + str(currYval) + "\' added to list!")
    if not currYval + 4 > 256:
        app.setSpinBox(Y, currYval + 4)
    try:
        if app.getAllListItems("Y list")[-2] == '256':
            app.setLabel("Info", "Maximum Y value reached.")
            app.removeListItem("Y list", "256")
    except Exception:
        pass

def rem_y(stuff):
    y = app.getSpinBox(Y)
    currYval = int(app.getSpinBox(Y))
    if app.getAllListItems("Y list"):
        if y in app.getAllListItems("Y list"):
            app.setSpinBox(Y, currYval - 4)
            #TODO: change the '4' value to a variable defined in the Gooey
            app.removeListItem("Y list", y)
            app.setLabel("Info", "Y value \'" + str(currYval) + "\' removed from list!")
        else:
            app.setLabel("Info", "Value not in list, can't remove it!")
    else:
        app.setLabel("Info", "List is empty! Can't remove nothing!")

def dirsel(name):
    currentFolder = app.directoryBox("whatever", "C:/Users/Elon/AppData/Roaming/.minecraft/other_versions/forge_1.9.4/saves/IronFarm1.8/data")
    if currentFolder is not None:
        global currFolder
        app.setLabel("CFolder", "Current folder: \n" + currentFolder)
        currFolder = currentFolder
        app.setLabel("Info", "Directory changed!")

def plot(schnitzel):
    nvillages = int(app.getEntry(NUM_VILLAGES))
    doorspervillage = int(app.getEntry(TOTAL_DOORS_PER_VILLAGE))
    doorsspace = int(app.getEntry(SPACE_BETWEEN_DOORS))
    x1 = int(app.getEntry(X_LOW))
    z1 = int(app.getEntry(Z_LOW))
    y = int(app.getSpinBox(Y))
    axis = app.getRadioButton("axis")
    coords = VillagesNBT.village_doors_coordinates(x1, nvillages, y, z1, doorspervillage / 2, doorsspace, axis)
    plotplotplotplotplot(coords)
    app.setLabel("Info", "Simulation complete!")
    return

def stop(k):
    cleanup()

    app.stop()

img = Image.new('RGB', (1, 1))
img.putdata([])
img.save('template.png')

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

app.startLabelFrame("Y Coordinates", 4, 0, 3)
app.addButton("Add Y coord to the list", add_y)
app.addListBox("Y list", [], 0, 1)
app.addButton("Remove Y coord from the list", rem_y, 0, 2)
app.stopLabelFrame()

app.addLabel("Info", "Startup complete! ", 7, 1, 3)

app.setEntry(NUM_VILLAGES, 32)
app.setEntry(TOTAL_DOORS_PER_VILLAGE, 22)
app.setEntry(SPACE_BETWEEN_DOORS, 19)
app.setEntry(X_LOW, -669)
app.setEntry(Z_LOW, -221)
app.setSpinBox(Y, 76)

app.addLabel("empty1", "\t\t\t", 0, 3)
app.addLabel("empty2", "\t\t\t\t\t\t\t\t\t", 0, 10)
app.addButton("Select The Villages.dat Folder", dirsel, 0, 7, 100)
app.addLabel("CFolder", "Current folder: \n" + currFolder, 1, 7, 100)

app.startLabelFrame("Axis along which a single village is created:", 2, 7, 1000)
app.addRadioButton("axis", "X")
app.addRadioButton("axis", "Z", 0, 1)
app.stopLabelFrame()

app.startLabelFrame("Backup Village file?", 3, 7, 1000)
app.addRadioButton("backup", "Yes")
app.addRadioButton("backup", "No", 0, 1)
app.setRadioButton("backup", "No")
app.stopLabelFrame()

app.addButton("Start", startthread, 7, 0)
app.addButton("Simulate", plot, 5, 0)
app.addButton("Exit", stop, 7, 7, 1000)

app.startSubWindow("simimg")
app.addImage("simimg", "template.png")
app.stopSubWindow()

app.setStretch("both")
app.go()

# bananaprofiler.stop()
# bananaprofiler.close()
# stats = hotshot.stats.load("banana.prof")
# stats.sort_stats('time', "cumulative")
# stats.print_stats(50)