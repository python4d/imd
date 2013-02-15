#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Créé le 28 nov. 2012
Code minimum pour créer l'application IMD3D et lancer l'interface
Mode debug ne permet pas de pour bénéficier du mulprocessing (cf MainApp.py et NoteBook.py)
@author: Python4D/Dynamic3D
@version: alpha
'''
from IMD3D import cIMD3D

if __name__ == '__main__':
  #import pydevd;pydevd.settrace()
  AppIMD3D=cIMD3D(debug=True)
  AppIMD3D.run()
  