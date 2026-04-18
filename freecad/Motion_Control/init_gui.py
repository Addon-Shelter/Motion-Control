# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileNotice: Part of the Motion Control addon.

from FreeCAD import Gui
from os import path


class Motion_Control(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """

    from freecad.Motion_Control import ICONPATH
    MenuText = "Motion Control"
    ToolTip = "OPC UA Connector"
    Icon = path.join(ICONPATH,'Addon.svg')

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """
        This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        import freecad.Motion_Control.Commands.Init
        import freecad.Motion_Control.Commands.Axes
        import freecad.Motion_Control.Commands.Actuators
        
        self.toolbox = ['Motion_Control_LinkToOpcUa', 'Motion_Control_AxisSetup', 'Motion_Control_ActuatorSetup']

        self.appendToolbar("Tools", self.toolbox)
        self.appendMenu("Tools", self.toolbox)

    def Activated(self):
        '''
        code which should be computed when a user switches to this workbench
        '''
        pass

    def Deactivated(self):
        '''
        code which should be computed when this workbench is deactivated
        '''
        pass


Gui.addWorkbench(Motion_Control())
