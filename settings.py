# Settings window
import maya.cmds as cmds
from utility import *
import preferences


@window
class SettingsWindow(object):  # Settings window window

    def __init__(self):
        self.GUI = {}  # Store GUI elements
        self.prefs = preferences.Preferences()  # Preferences

        title = "Settings:"
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
        path = FileSelect()
        print "Set template to: %s." % path
        self.prefs.save("template_path", path)
        self.updateTemplate()

    def setPoseFolder(self, *none):
        path = FileSelect()
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
