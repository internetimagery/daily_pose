# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
#reload(__import__('daily_pose'))
import app
import maya.cmds as cmds
import json, os, utility, desktop, shutil


def singleton(cls):  # Only keep one window open at a time
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance


@singleton
class Preferences(object):

    def __init__(self):
        self.path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "prefs.json")
        try:
            f = open(self.path, "r")
            data = json.load(f)
            self.data = data if data else {}
            f.close()
        except IOError:
            self.data = {}

    def load(self, key):
        return self.data.get(key, None)

    def save(self, key, val):
        self.data[key] = val
        try:
            f = open(self.path, "w")
            json.dump(self.data, f, encoding="utf-8", indent=4)
            f.close()
        except IOError, e:
            print e


@singleton
class MainWindow(object):  # Main GUI window

    def __init__(self):
        self.GUI = {}  # Store GUI elements
        title = "Pose a Day CHALLENGE"
        self.prefs = Preferences()
        self.settings = ""  # Holder for settings window

        self.GUI['window'] = cmds.window(title=title, rtf=True, s=False)
        # LEFT ROW
        self.GUI["layout1"] = cmds.rowColumnLayout(nc=2)
        self.GUI['layout2'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["text1"] = cmds.text(label="STUFF IN HERE")

        cmds.setParent("..")
        # RIGHT ROW
        self.GUI["layout3"] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["button1"] = cmds.button(label="PUSH ME", h=30, c=self.dummy)
        cmds.separator()
        self.GUI["button2"] = cmds.button(label="PUSH ME TOO", h=30, c=self.dummy)
        self.GUI["button3"] = cmds.button(label="Settings", h=30, c=self.openSettings)

        allowed_areas = ['right', 'left']
        self.GUI['dock'] = cmds.dockControl(a='left', content=self.GUI['window'], aa=allowed_areas, fl=True, l=title, fcc=self.moveDock, vcc=self.closeDock)

        location = self.getLocation()
        if location == 'float':
            cmds.dockControl(self.GUI['dock'], e=True, fl=True)
        elif location in allowed_areas:
            cmds.dockControl(self.GUI['dock'], e=True, a=location)

    def moveDock(self):  # Update dock location information
        if cmds.dockControl(self.GUI['dock'], q=True, fl=True):
            self.setLocation("float")
            print "Floating Dock."
        else:
            area = cmds.dockControl(self.GUI['dock'], q=True, a=True)
            self.setLocation(area)
            print "Docking %s." % area

    def closeDock(self, *loop):
        visible = cmds.dockControl(self.GUI['dock'], q=True, vis=True)
        if not visible and loop:
            cmds.scriptJob(ie=self.closeDock, p=self.GUI['dock'], ro=True)
        elif not visible:
            self.cleanUp()
            cmds.deleteUI(self.GUI['dock'], control=True)
            print "Window closed."

    def getLocation(self):
        return self.prefs.load("location")

    def setLocation(self, location):
        self.prefs.save("location", location)

    def openSettings(self, *none):
        self.settings = SettingsWindow()

    def cleanUp(self):
        try:
            settings = self.settings.GUI["window"]
            if cmds.window(settings, ex=True):
                cmds.deleteUI(settings, wnd=True)
        except AttributeError as e:
            pass

    def dummy(self, arg):
        print "hello"


@singleton
class SettingsWindow(object):  # Settings window window

    def __init__(self):
        self.GUI = {}  # Store GUI elements
        title = "Settings:"
        self.prefs = Preferences()

        self.GUI['window'] = cmds.window(title=title, rtf=True, s=False)
        self.GUI['layout1'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["text1"] = cmds.text(label="Settings")
        cmds.separator()
        self.GUI["button1"] = cmds.button(label="Open Template", h=50, c=self.openTemplate)
        self.GUI["layout1"] = cmds.rowColumnLayout(nc=2)

        self.GUI['layout2'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["button2"] = cmds.button(label="Set Template File", h=30, c=self.setTemplate)
        self.GUI["button3"] = cmds.button(label="Set Pose Folder", h=30, c=self.setPoseFolder)
        cmds.setParent('..')

        self.GUI['layout3'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["text2"] = cmds.text(h=30, label="STUFF IN HERE")
        self.GUI["text3"] = cmds.text(h=30, label="MORE STUFF HERE")

        self.updateTemplate()
        self.updatePoseFolder()

        cmds.showWindow(self.GUI["window"])

    def openTemplate(self, *none):
        path = self.prefs.load("template_path")
        if os.path.exists(path):
            desktop.open(path)
        else:
            cmds.messageBox(title="Uh oh...", message="Could not find your template file...\n%s" % path)

    def setTemplate(self, *none):
        path = utility.FileSelect()
        print "Set template to: %s." % path
        self.prefs.save("template_path", path)
        self.updateTemplate()

    def setPoseFolder(self, *none):
        path = utility.FileSelect()
        print "Set pose folder to %s." % path
        self.prefs.save("pose_path", path)
        self.updatePoseFolder()

    def updateTemplate(self):
        template = self.prefs.load("template_path")
        template = template if template else "{{ Default Template }}"
        cmds.text(self.GUI["text2"], e=True, label=template)

    def updatePoseFolder(self):
        pose_folder = self.prefs.load("pose_path")
        pose_folder = pose_folder if pose_folder else "Please add a Folder."
        cmds.text(self.GUI["text3"], e=True, label=pose_folder)


def init():
    # Initialize everything
    template = os.path.join(os.path.dirname(os.path.realpath(__file__)), "template")
    if not os.path.exists(template):
        os.makedirs(template)
    prefs = Preferences()
    if not prefs.load("template_path"):
        prefs.save("template_path", template)

init()
