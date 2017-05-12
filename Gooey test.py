from appJar import gui
a = 5
def button91(name):
    global a
    a -= 1
    app.setBg("red")
    app.setButton("Button", a)
    if a == 0:
        app.stop()


app = gui("Helloooooo")
app.addLabel("Title", "Hello world")
app.addLabel("Title1", "Banana is tasty")
app.setBg("white")
app.setFont(20, "Calibri")
app.setLabelBg("Title", "yellow")
app.setLabelFg("Title", "black")
app.setGeom("1280x720")

app.addButton("Button", button91)

app.go()
pass