#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
IMD3D is the Python package for the Project IMD3D
This package contains specific package/module for this project (ie vtk2obj.py)
and contains some known unmodify or modify package/modules (ie pyvtk package)
"""

__author__ = "Damien Samain (dmien.samain@python4d.com)"
__license__ = "Dynamic3D copyright"
from __version__ import __version__

#Liste les fonctions visible du package IMD3D (from IMD3D import *)
__all__=['cIMD3D']

from MainApp import cIMD3D



