# Automate some daily pose tasks. Such as creating a folder and opening it up. All from maya
import app
import maya.cmds as cmds

# Fancypants GUI
class GUI(object):
    def __init__(self):
        self.GUI = {}
        self.GUI["window"] = cmds.window(title = "Pose a day CHALLENGE", rtf = True, s = False)
        self.GUI["layout1"] = cmds.rowColumnLayout(nc = 2)

        self.GUI["layout2"] = cmds.columnLayout(adjustableColumn = True, w = 120)
        self.GUI["text1"] = cmds.text(label = "STUFF IN HERE")

        cmds.setParent("..")

        self.GUI["layout3"] = cmds.columnLayout(adjustableColumn = True)
        self.GUI["button1"] = cmds.button(label = "PUSH ME", h=30, c=self.dummy)
        cmds.separator()
        self.GUI["button2"] = cmds.button(label = "PUSH ME TOO", h=30, c=self.dummy)

        cmds.setParent("..")

        cmds.setParent("..")
        cmds.showWindow( self.GUI["window"] )

    def dummy(self, arg):
        return
