# Save preferences
from utility import window
import json, os


@window
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
