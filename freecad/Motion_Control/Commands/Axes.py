# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Motion Control addon.

from FreeCAD import activeDocument , Gui
from PySide6 import QtCore, QtWidgets
from os import path

from freecad.Motion_Control import ICONPATH, AXES

from ..Axis.Widgets import AxisWidgets
from ..Settings import Settings

__dir__ = path.dirname(__file__)
__axis_params__ = path.join(__dir__, 'Axis','Parameters.fcmc')

class AxisPanel:

    def __init__(self, widget, count):
        #number of axes
        self.axes = count

        #attribute for storing all settings widgets
        self.axis_list = []

        # instance of Settings
        self.settings = Settings()

        # some variables
        self.poll_rate = 50
        
        #reference to QWidget
        self.form = widget

        #Grid Layout
        layout = QtWidgets.QGridLayout(self.form)

        # ---- row 0: settings column headers
        # OPC UA side:
        self.opcLabel = QtWidgets.QLabel("Node Id")
        # FreeCad side:
        self.multiLabel = QtWidgets.QLabel("Factor")
        self.docLabel = QtWidgets.QLabel("Document")
        self.objLabel = QtWidgets.QLabel("LCS")
        self.vectorLabel = QtWidgets.QLabel("Offset")
        self.typeLabel = QtWidgets.QLabel("Type")

        # row 0, column 0, rowspan 1, colspan 3
        layout.addWidget(self.opcLabel,0,0,1,3)
        # row 0, column 4, rowspan 1, colspan 1
        layout.addWidget(self.multiLabel,0,4,1,1)
        # row 0, column 5, rowspan 1, colspan 2
        layout.addWidget(self.docLabel,0,5,1,2)
        # row 0, column 7, rowspan 1, colspan 2
        layout.addWidget(self.objLabel,0,7,1,2)
        # row 0, column 9, rowspan 1, colspan 2
        layout.addWidget(self.vectorLabel,0,9,1,1)
        # row 0, column 5, rowspan 1, colspan 2
        layout.addWidget(self.typeLabel,0,10,1,1)

        # ---- row 1..n: settings widgets
        if self.axes > 0:
            for i in range(self.axes):
                # create setting widget and gather them in a list
                self.axis_list.append(AxisWidgets(i)) 
                # starting column index
                col = 0 
                # list of column widths 
                col_spans = [2,1,1,1,2,2,1,1] 
                # add widgets to layout with their respective column width, increment the column index accordingly
                for w in range(len(self.axis_list[0].widgets)):
                    layout.addWidget(self.axis_list[i].widgets[w],1+i,col,1,col_spans[w])
                    col += col_spans[w]
        else:
            # no axis configured
            defaultLabel = QtWidgets.QLabel('No axis configured in .ini')
            layout.addWidget(defaultLabel)

        #load previous settings from file params.fcmc
        self.settings.load_axis_settings(self.axis_list)
        

    def accept(self):
        if self.axes > 0:
            self.settings.save_axis_settings(self.axis_list)
        Gui.Control.closeDialog() #close the dialog

    
    def reject(self):
        Gui.Control.closeDialog() #close the dialog
    

class _AxisSetup:
    def Activated(self):
        #create and show the panel
        baseWidget = QtWidgets.QWidget()
        panel = AxisPanel(baseWidget, AXES)
        Gui.Control.showDialog(panel)

    def GetResources(self):
        # icon and command information
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Motion_Control_AxisSetup',
            'Axis settings dialog')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Motion_Control_AxisSetup',
            'Link OPC UA nodes (non-boolean) to FreeCAD objects')
        return {
            'Pixmap': path.join(ICONPATH, "Axes.svg"),
            'MenuText': MenuText,
            'ToolTip': ToolTip}

    def IsActive(self):
        # The command will be active if there is an active document
        return not activeDocument is None


Gui.addCommand('Motion_Control_AxisSetup', _AxisSetup())
