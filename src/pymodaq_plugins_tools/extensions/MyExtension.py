from qtpy import QtWidgets, QtCore


import numpy as np
from pymodaq_gui import utils as gutils
from pymodaq_utils.config import Config, ConfigError
from pymodaq_utils.logger import set_logger, get_module_name
from pymodaq_gui.utils import DockArea, Dock

from pymodaq.utils.config import get_set_preset_path
from pymodaq.extensions.utils import CustomExt
import pyqtgraph

from pymodaq_plugins_rigi.utils import Config as PluginConfig
from pymodaq_data.data import DataToExport
from pymodaq_data.data import (Axis, DataToExport, DataFromRoi, DataRaw,
                               DataDistribution, DataWithAxes)

from pymodaq_gui.plotting.data_viewers import viewer0D, viewer1D, viewer2D


logger = set_logger(get_module_name(__file__))

main_config = Config()
plugin_config = PluginConfig()

EXTENSION_NAME = "TEST EXTENSION" 
CLASS_NAME = 'MyExtension' 

class MyExtension(CustomExt):


    
    params = []

    

    def __init__(self, parent: gutils.DockArea, dashboard):
        super().__init__(parent, dashboard)

        # info: in an extension, if you want to interact with ControlModules you have to use the
        # object: self.modules_manager which is a ModulesManager instance from the dashboard

        self.plot_widgets = []
        self.setup_ui()


    def setup_docks(self):
        """Mandatory method to be subclassed to setup the docks layout

        Examples
        --------
        >>>self.docks['ADock'] = gutils.Dock('ADock name')
        >>>self.dockarea.addDock(self.docks['ADock'])
        >>>self.docks['AnotherDock'] = gutils.Dock('AnotherDock name')
        >>>self.dockarea.addDock(self.docks['AnotherDock'''], 'bottom', self.docks['ADock'])

        See Also
        --------
        pyqtgraph.dockarea.Dock
        """

        self.dock_command = Dock('Scan Command')
        self.viewer_dock = Dock("Test")
        self.dockarea.addDock(self.dock_command)

        # viewer_widget = QtWidgets.QWidget()
        # view = viewer2D.Viewer2D(parent=viewer_widget, title="test")
        # self.viewer_dock.addWidget( viewer_widget )

        x = np.linspace(0,100,10000); y = np.sin(x)

        # Main Widgets
        main_widget = QtWidgets.QWidget()

        # Sub Widgets
        small_plot_widget = QtWidgets.QWidget(); view = viewer2D.Viewer2D(parent=small_plot_widget, title="2D"); self.plot_widgets.append(view)
        small_plot_widget.setFixedSize(300,300)

        line_plot_widget = QtWidgets.QWidget(); line = viewer0D.Viewer0D(parent=line_plot_widget, title="0D"); self.plot_widgets.append(line)

        big_plot_widget = pyqtgraph.PlotWidget(title="Big graph"); big_plot_widget.plot(x, y)

        button_widget = QtWidgets.QPushButton(text="Set Boundaries"); button_widget.clicked.connect( self.define_region )
        button_widget.setMaximumHeight(50)

        # label_widget = QtWidgets.QInputDialog(); label_widget.setText("Tut")
        # label_widget.setMaximumHeight(50)
        label_widget = QtWidgets.QInputDialog()

        


        # Create Splitters
        h_splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        left_splitter = QtWidgets.QSplitter(QtCore.Qt.Vertical)

        # Assemble splitters
        left_splitter.addWidget(button_widget)
        left_splitter.addWidget(label_widget)
        left_splitter.addWidget(small_plot_widget)
        # left_splitter.setSizes([300, 200])

        h_splitter.addWidget(left_splitter)
        h_splitter.addWidget(line_plot_widget)
        h_splitter.setSizes([300, 700])

        # Layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(h_splitter)
        main_widget.setLayout(layout)

        self.dock_command.addWidget(main_widget)



    def setup_actions(self):
        """Method where to create actions to be subclassed. Mandatory

        Examples
        --------
        >>> self.add_action('quit', 'Quit', 'close2', "Quit program")
        >>> self.add_action('grab', 'Grab', 'camera', "Grab from camera", checkable=True)
        >>> self.add_action('load', 'Load', 'Open', "Load target file (.h5, .png, .jpg) or data from camera"
            , checkable=False)
        >>> self.add_action('save', 'Save', 'SaveAs', "Save current data", checkable=False)

        See Also
        --------
        ActionManager.add_action
        """
        #add_action(short_name, name, icon_name, tip, checkable, checked ,toolbar ,menu  ,visible ,shortcut ,auto_toolbar ,auto_menu ,enabled):
        self.add_action('quit', 'Quit', 'close2', "Quit program")
        self.add_action('grab', 'Grab', 'camera', "Grab from camera", checkable=True)
        self.add_action('load', 'Load', 'Open', "Load target file (.h5, .png, .jpg) or data from camera" , checkable=False)
        self.add_action('save', 'Save', 'SaveAs', "Save current data", checkable=False)


    def connect_things(self):
        """Connect actions and/or other widgets signal to methods"""
        self.connect_action('quit', quit)
        
        self.modules_manager.selected_detectors_name = ["Det 00"]
        self.modules_manager.connect_detectors()
        self.modules_manager.det_done_signal.connect(self.receive_data)


    def receive_data(self, data : DataToExport):
        region_data = data[0].data[0]
        integrated_data = data[1].data[0]

        self.plot_widgets[0].show_data( DataRaw(name='mydata', distribution='spread', data=[ region_data ]) )
        self.plot_widgets[1].show_data( DataRaw(name='mydata', distribution='spread', data=[ integrated_data ]) )
        # self.plot_widgets[0].plot(region_data)


    def define_region(self):
        self.modules_manager.grab_data() 



    def setup_menu(self, menubar: QtWidgets.QMenuBar = None):
        """Non mandatory method to be subclassed in order to create a menubar

        create menu for actions contained into the self._actions, for instance:

        Examples
        --------
        >>>file_menu = menubar.addMenu('File')
        >>>self.affect_to('load', file_menu)
        >>>self.affect_to('save', file_menu)

        >>>file_menu.addSeparator()
        >>>self.affect_to('quit', file_menu)

        See Also
        --------
        pymodaq.utils.managers.action_manager.ActionManager
        """
        file_menu = menubar.addMenu('File')
        self.affect_to('load', file_menu)
        self.affect_to('save', file_menu)

        file_menu.addSeparator()
        self.affect_to('quit', file_menu)


    def value_changed(self, param):
        """ Actions to perform when one of the param's value in self.settings is changed from the
        user interface

        For instance:
        if param.name() == 'do_something':
            if param.value():
                print('Do something')
                self.settings.child('main_settings', 'something_done').setValue(False)

        Parameters
        ----------
        param: (Parameter) the parameter whose value just changed
        """
        pass


def main():
    # from pymodaq.utils.gui_utils.utils import mkQApp
    from pyqtgraph import mkQApp
    from pymodaq.utils.gui_utils.loader_utils import load_dashboard_with_preset
    from pymodaq.utils.messenger import messagebox

    app = mkQApp(EXTENSION_NAME)
    try:
        # preset_file_name = plugin_config('presets', f'preset_for_{CLASS_NAME.lower()}')
        preset_file_name = "preset_default"
        print(preset_file_name)
        load_dashboard_with_preset(preset_file_name, EXTENSION_NAME)
        app.exec()

    except ConfigError as e:
        messagebox(f'No entry with name f"preset_for_{CLASS_NAME.lower()}" has been configured'
                   f'in the plugin config file. The toml entry should be:\n'
                   f'[presets]'
                   f"preset_for_{CLASS_NAME.lower()} = {'a name for an existing preset'}"
                   )


if __name__ == '__main__':
    main()
