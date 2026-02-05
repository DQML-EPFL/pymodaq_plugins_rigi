pymodaq_plugins_tools
#####################

.. the following must be adapted to your developed package, links to pypi, github  description...

.. .. image:: https://img.shields.io/pypi/v/pymodaq_plugins_template.svg
..    :target: https://pypi.org/project/pymodaq_plugins_template/
..    :alt: Latest Version

.. .. image:: https://readthedocs.org/projects/pymodaq/badge/?version=latest
..    :target: https://pymodaq.readthedocs.io/en/stable/?badge=latest
..    :alt: Documentation Status

.. .. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/workflows/Upload%20Python%20Package/badge.svg
..    :target: https://github.com/PyMoDAQ/pymodaq_plugins_template
..    :alt: Publication Status

.. .. image:: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml/badge.svg
..     :target: https://github.com/PyMoDAQ/pymodaq_plugins_template/actions/workflows/Test.yml


The SwissTHz Rigi Camera is a great camera for imaging THz beams.
However, this camera does not allow direct interfacing via python, making data aquisition complicated.
This plugin circonvents this by using python to take screenshots of the displayed labview interface to extract the camera data.


Authors
=======

* Malo Hervé  (malo.herve@epfl.ch)

Instruments
===========

The [Rigi Camera](https://www.swissterahertz.com/rigicamera) is needed for imaging the beam, however this plugin may work for any other purpose where extracting visual data from a screen display is needed.


Installation instructions
=========================

* PyMoDAQ 5.0.18, running with Python v3.11.*.
* Windows 10/Windows 11
