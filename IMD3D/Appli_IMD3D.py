#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Cr�� le 28 nov. 2012
Code minimum pour cr�er l'application IMD3D et lancer l'interface
Mode debug ne permet pas de pour b�n�ficier du mulprocessing (cf MainApp.py et NoteBook)
@author: Python4D/Dynamic3D
'''
from IMD3D import cIMD3D


if __name__ == '__main__':
  AppIMD3M=cIMD3D(debug=True)
  AppIMD3M.run()