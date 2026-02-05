
from typing import Union, List, Dict
from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)

from pymodaq_utils.utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq_gui.parameter import Parameter

from pymodaq_plugins_tools.hardware.Click_and_Write_Master import Click_and_Write_Master

from pyqtgraph.parametertree.parameterTypes import *
import copy

import PyQt5.QtWidgets as QtWidgets

class DAQ_Move_Clicks(DAQ_Move_base):
    """ Instrument plugin class for an actuator.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Move module through inheritance via
    DAQ_Move_base. It makes a bridge between the DAQ_Move module and the Python wrapper of a particular instrument.

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.

    """
    is_multiaxes = False
    _axis_names: Union[List[str], Dict[str, int]] = ['Wavelength']
    _controller_units: Union[str, List[str]] = 'nm'
    _epsilon: Union[float, List[float]] = 0.01
    data_actuator_type = DataActuatorType.DataActuator

    params = [
             {'title':'Wait Time', 'name':'wait', 'type':'int', 'suffix':'ms', 'value':0.1, 'default':0.1},
             {'title':'Define Sequence', 'name':'define', 'type':'bool_push', 'value':False, 'default':False, 'children':[
                 {'title':'Sample', 'name':'sample', 'type':'str', 'value':"This is a Test", 'readonly':True}
             ]},
             
             ] + comon_parameters_fun(is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)


    def ini_attributes(self):
        self.controller : Click_and_Write_Master = None

        self.sample_opts = self.settings.child("define", "sample").opts
        self.settings.child("define", "sample").hide()


    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = DataActuator(data=self.controller.get_current_value(), units=self.axis_unit)
        return pos


    def close(self):
        """Terminate the communication protocol"""
        if self.is_master:
             self.controller.close_communication()


    def commit_settings(self, param: Parameter):
        if param.name() == 'define':
            sequence = self.controller.define_sequence()
            self.update_sequence(sequence)
            self.settings.child("define").setValue( False ) 
        else: pass


    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        if self.is_master:
            self.controller = Click_and_Write_Master() 
            initialized = self.controller.open_communication()

        else:
            self.controller = controller
            initialized = True

        info = "Whatever info you want to log"
        return info, initialized


    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """
        self.controller.execute()


    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        self.controller.execute()


    def move_home(self):
        """Call the reference method of the controller"""
        self.emit_status(ThreadCommand('Update_Status', ['Some info you want to log']))


    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""
        pass

    def update_sequence(self, sequence):
        
        self.settings.child("define").clearChildren()   # TODO: Not working
        for i, action in enumerate(sequence):
            opts = self.sample_opts.copy()
            opts["name"] = f"step{i}"
            opts["title"] = f"Step {i}"
            opts["value"] = f"{action}"
            opts["visible"] = True
            param = TextParameter(**opts)
            self.settings.child("define").addChild(param)






if __name__ == '__main__':
    main(__file__)

