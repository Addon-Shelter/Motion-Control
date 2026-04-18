# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Motion Control addon.

from sys import path as paths
from os import path

from .version import __version__

ICONPATH = path.join(path.dirname(__file__), "resources")

# read number of axes, actuators from file
with open(path.join(path.dirname(__file__), "fcmcua.ini")) as settings:
    strng = settings.read()
    __axes__ = __actuators__ = 0
    for s in strng.split():
        if __axes__ == 0:
            __axes__ = int((s[len("AxNum="):] if (s[:len("AxNum=")] == "AxNum=") else "0" ))
        if __actuators__ == 0:
            __actuators__ = int((s[len("ActNum="):] if (s[:len("ActNum=")] == "ActNum=") else "0" ))

AXES = __axes__
ACTUATORS = __actuators__

# add paths to sys.path so that FreeCAD's python interpreter finds all files
py_path = path.join(path.dirname(__file__), "dependencies")

if path.exists(path.dirname(py_path)):
    paths.append(py_path)

wb_path = path.dirname(__file__)

if path.exists(path.dirname(wb_path)):
    paths.append(wb_path)
