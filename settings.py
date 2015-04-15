# Settings window
import maya.cmds as cmds
from utility import *
import preferences


@window
class SettingsWindow(object):  # Settings window window

    def __init__(self):
        self.GUI = {}  # Store GUI elements
        self.prefs = preferences.Preferences()  # Preferences

        def button(text, command, icon):
            image = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "icons", icon)
            ui = []
            ui.append(cmds.rowLayout(ad2=2, nc=2))
            ui.append(cmds.symbolButton(image=image, h=50, w=50, c=command))
            ui.append(cmds.button(label=text, h=50, c=command))
            cmds.setParent("..")
            return ui

        title = "Settings:"
        self.GUI['window'] = cmds.window(title=title, rtf=True, s=False)
        self.GUI['layout1'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["text1"] = cmds.text(label="Settings")
        cmds.separator()
        self.GUI["button1"] = cmds.button(label="Open Template", h=50, c=self.openTemplate)
        self.GUI["layout1"] = cmds.rowColumnLayout(nc=2)

        self.GUI['layout2'] = cmds.columnLayout(adjustableColumn=True, bgc=[0.8, 0.8, 0.8])
        self.GUI["button2"] = button("Set Template File", self.setTemplate, "Upload-Folder-icon.png")
        self.GUI["button3"] = button("Set Pose Folder", self.setPoseFolder, "Edit-Folder-icon.png")
        # self.GUI["check1"] = cmds.symbolCheckBox(ann="Reminder", h=50, w=50, oni=imgOn, ofi=imgOff, cc=self.toggleReminder)
        self.GUI["check1"] = cmds.iconTextCheckBox(l="Reminder", style='iconAndTextHorizontal', h=50, al="center", cc=self.toggleReminder)
        cmds.setParent('..')

        self.GUI['layout3'] = cmds.columnLayout(adjustableColumn=True)
        self.GUI["text2"] = cmds.text(h=50, label="STUFF IN HERE")
        self.GUI["text3"] = cmds.text(h=50, label="MORE STUFF HERE")
        self.GUI["text4"] = cmds.text(h=50, label="Trigger reminder popups each day.")

        self.updateTemplate()
        self.updatePoseFolder()
        self.updateReminder()
        cmds.setParent('..')

        cmds.showWindow(self.GUI["window"])

    def openTemplate(self, *none):
        path = self.prefs.load("template_path")
        if os.path.exists(path):
            FolderOpen(path)
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

    def toggleReminder(self, value):
        print "Reminder set to %s" % ("on" if value else "off")
        self.prefs.save("daily_reminder", value)
        self.updateReminder()

    def updateReminder(self):
        value = self.prefs.load("daily_reminder")
        value = value if value else False
        imgOn = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "icons", "calendar-clock-on-small.png")
        imgOff = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images", "icons", "calendar-clock-off-small.png")
        text = "Reminders are on." if value else "Click to trigger a Pose reminder each day."
        img = imgOn if value else imgOff
        cmds.text(self.GUI["text4"], e=True, label=text)
        cmds.iconTextCheckBox(self.GUI["check1"], e=True, v=value, i=img)

    def updateTemplate(self):
        template = self.prefs.load("template_path")
        template = template if template else "{{ Default Template }}"

        cmds.text(self.GUI["text2"], e=True, label="   %s   " % template)

    def updatePoseFolder(self):
        pose_folder = self.prefs.load("pose_path")
        pose_folder = pose_folder if pose_folder else "Please add a Folder."
        cmds.text(self.GUI["text3"], e=True, label="   %s   " % pose_folder)
