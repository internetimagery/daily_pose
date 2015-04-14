# Helper utility functions
import maya.cmds as cmds
import os, re, sys

# List all files in directory


def list(path, hidden=False):  # Show hidden?
    result = []
    regex = re.compile("%s/?" % path)  # Remove base path for relative URL's
    for root, dirs, files in os.walk(path):
        # Don't go into hidden folders
        for dir in dirs:
            if dir[0] == "." and hidden is False:
                dirs.remove(dir)
        root = re.sub(regex, "", root)
        for file in files:
            # Ignore hidden files
            if not file[0] == "." or hidden:
                result.append(os.path.join(root, file))
    return result


# Select a folder prompt


def FileSelect():
    return cmds.fileDialog2(ds=2, cap="Select a Folder.", fm=3, okc="Select")[0]


# Only allow one single instance of class


def window(cls):  # Only keep one window open at a time
    instances = {}

    def getinstance():
        if (cls in instances and sys.getrefcount(instances[cls]) < 3) or cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance
