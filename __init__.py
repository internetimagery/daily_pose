# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
#reload(__import__('daily_pose'))
import maya.cmds as cmds
import os, desktop, shutil, datetime, settings
from utility import *
from preferences import Preferences


@window
class MainWindow(object):  # Main GUI window

    def __init__(self):
        self.GUI = {}  # Store GUI elements
        title = "Pose a Day CHALLENGE"
        self.prefs = preferences.Preferences()
        self.date = datetime.date.today()  # Todays Date
        location = self.getLocation()
        allowed_areas = ['right', 'left']

        self.GUI['window'] = cmds.window(title=title, rtf=True, s=False)
        self.GUI["wrapper"] = cmds.columnLayout(adjustableColumn=True)

        allowed_areas = ['right', 'left']
        self.GUI['dock'] = cmds.dockControl(a='left', content=self.GUI['window'], aa=allowed_areas, l=title, fcc=self.moveDock, vcc=self.closeDock)

        if location == 'float':
            cmds.dockControl(self.GUI['dock'], e=True, fl=True)

        elif location in allowed_areas:
            cmds.dockControl(self.GUI['dock'], e=True, a=location)
            self.buildDockLayout()

    def buildFloatLayout(self):
        self.GUI["layout1"] = cmds.rowColumnLayout(nc=2, p=self.GUI["wrapper"])
        # LEFT ROW
        self.GUI['layout2'] = cmds.columnLayout(adjustableColumn=True, p=self.GUI["layout1"])
        self.updateImage(self.GUI["layout2"])
        # RIGHT ROW
        self.GUI["layout3"] = cmds.columnLayout(width=150,p=self.GUI["layout1"])
        self.updateButtons(self.GUI["layout3"])

    def buildDockLayout(self):
        self.GUI['layout2'] = cmds.columnLayout(adjustableColumn=True, p=self.GUI["wrapper"])
        self.updateImage(self.GUI["layout2"])
        self.updateButtons(self.GUI["layout2"])

    def purgeGUI(self, *args):
        children = cmds.layout(self.GUI["wrapper"], q=True, ca=True)
        if children:
            for ui in children:
                cmds.deleteUI(ui, lay=True)

    def updateImage(self, parent):
        img = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dailypose.jpg")
        self.GUI["image1"] = cmds.image(image=img, p=parent)

    def updateButtons(self, parent):
        self.GUI["button1"] = cmds.button(label="TODAYS POSE\n\n%s" % self.date, h=80, w=150, c=self.dummy, p=parent)
        cmds.separator(p=parent)
        self.GUI["button2"] = cmds.button(label="Settings", h=30, w=150, c=self.openSettings, p=parent)

    def moveDock(self):  # Update dock location information
        if cmds.dockControl(self.GUI['dock'], q=True, fl=True):
            self.setLocation("float")
            self.purgeGUI()
            self.buildFloatLayout()
        else:
            area = cmds.dockControl(self.GUI['dock'], q=True, a=True)
            self.setLocation(area)
            self.purgeGUI()
            self.buildDockLayout()

    def closeDock(self, *loop):
        visible = cmds.dockControl(self.GUI['dock'], q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=self.closeDock, p=self.GUI['dock'], ro=True)
        elif not visible:
            self.cleanUp()
            cmds.deleteUI(self.GUI['dock'], control=True)
            print "Window closed."

    def getLocation(self):
        dock = self.prefs.load("dock_location")
        return dock if dock else "float"

    def setLocation(self, location):
        self.prefs.save("dock_location", location)

    def openSettings(self, *none):
        self.GUI["settings"] = settings.SettingsWindow().GUI["window"]

    def cleanUp(self):
        try:
            if cmds.window(self.GUI["settings"], ex=True):
                cmds.deleteUI(self.GUI["settings"], wnd=True)
        except KeyError:
            pass

    def dummy(self, arg):
        print "hello"


def init():
    # Initialize everything
    template = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    if not os.path.exists(template):
        os.makedirs(template)
    prefs = preferences.Preferences()
    if not prefs.load("template_path"):
        prefs.save("template_path", template)

init()
