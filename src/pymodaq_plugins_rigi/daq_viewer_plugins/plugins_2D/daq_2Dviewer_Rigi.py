import numpy as np
from ...hardware.ScreenshotMaster import ScreenshotMaster
# pymodaq_plugins_rigi/src/pymodaq_plugins_rigi/hardware/ScreenshotMaster.py
# print(np.__version__)

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins

import keyboard
import pyautogui

class DAQ_2DViewer_Rigi(DAQ_Viewer_base):
    params = comon_parameters+[
        {'title':'Region Parameters',
         'name':'region',
         'type':'group',
         'children':[        
             {'title':'X Start', 'name':'x_start', 'type':'int', 'value':50, 'default':50 },
             {'title':'Y Start', 'name':'y_start', 'type':'int', 'value':55, 'default':55},
             {'title':'X End', 'name':'x_end', 'type':'int', 'value':1260, 'default':1260 },
             {'title':'Y End', 'name':'y_end', 'type':'int', 'value':960, 'default':960},
             ]},
        {'title':'Define Region TEST', 'name':'define', 'type':'bool_push', 'value':False, 'default':False},
        {'title':'Integrate over N', 'name':'integrate', 'type':'led_push', 'value':False, 'default':False},
        {'title':'N', 'name':'integrate_n', 'type':'int', 'value':100, 'default':100},
        ]


    def ini_attributes(self):
        region = (self.settings.child('region', 'x_start').value(), 
                    self.settings.child('region', 'y_start').value(), 
                    self.settings.child('region', 'x_end').value(), 
                    self.settings.child('region', 'y_end').value())        
        
        self.controller: ScreenshotMaster = ScreenshotMaster(region=region)



    def commit_settings(self, param: Parameter):
        """Apply the consequences of a change of value in the detector settings """

        if param.name() == "x_start" or "x_end" or "y_start" or "y_end":
            region = (self.settings.child('region', 'x_start').value(), 
                self.settings.child('region', 'y_start').value(), 
                self.settings.child('region', 'x_end').value(), 
                self.settings.child('region', 'y_end').value())
            self.controller.set_region(region)

        
        if param.name() == "define":
            print("Defining Region")
            points = {}

            while len(points)!=2:
                if keyboard.is_pressed('ctrl'):
                    points[ pyautogui.position() ] = ""

            points = [key for key in points.keys() ]
            region = (points[0][0], points[0][1], points[1][0], points[1][1])
            self.controller.set_region(region)


    def ini_detector(self, controller=None):
        """Detector communication initialization """

        initialized = True
        info = "Rigi Initialized (Not really I can't read the .dll)"
        return info, initialized

    def close(self):
        """Terminate the communication protocol"""
        return " "


    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """

        N = 1
        if self.settings.child('integrate').value():
            N = self.settings.child('integrate_n').value()

        intensity_list = []
        for i in range(N):
            gray, intensity = self.controller.start_a_grab_snap()
            intensity_list.append(intensity)

        data_to_export = []
        data_to_export.append(DataFromPlugins(name='Region', data=np.flip(gray[::2, ::2], axis=0), dim='Data2D', labels=['Region Observed'], do_plot=True, do_save=False))
        data_to_export.append(DataFromPlugins(name='Intensity', data=np.mean(intensity_list), dim='Data0D', labels=["Integrated Intensity"], do_plot=True, do_save=True))

        data = DataToExport('Picoscope', data=data_to_export)

        self.dte_signal.emit(data)

        #########################################################




    def callback(self):
        """optional asynchrone method called when the detector has finished its acquisition of data"""
        data_tot = self.controller.your_method_to_get_data_from_buffer()
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Mock1', data=data_tot,
                                                                dim='Data0D', labels=['dat0', 'data1'])]))

    def stop(self):
        """Stop the current grab hardware wise if necessary"""
        self.emit_status(ThreadCommand('Update_Status', ['Stop']))
        # ##############################
        return ''


if __name__ == '__main__':
    main(__file__)
