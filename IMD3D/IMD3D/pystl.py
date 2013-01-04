#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Créé le 21 déc. 2012
Importer un fichier STL
@note: http://farmerjoe.info/batch_stl/1.0/batch_stl.py
@author: Python4D/damien
'''


from struct import unpack
import os.path

class cSTL(object):
  """
  Class cSTL utilisé pour extraire les faces d'un fichier STL
  Le fichier (filename) peut-être de format (fileformat)
  @param filename: nom du fichier STL
  """
  def __init__(self,filename):
    self.set_filename(filename)
  def set_filename(self, filename):
    if not os.path.isfile(filename):
      print u"Création de l'objet cSTL impossivle >> Error: file %s not found."%filename
      self._filename = None
    else:
      self._filename = filename
    
  ######################################################
  # Read STL Triangle Format
  ######################################################
  
  def read(self,fileformat='a',scale=1):
    """lecture et extraction des data du fichier STL
    @param fileformat: 'b' pour un fichier binaire STL sinon traité comme un ASCII
    @param scale: facteur multipliant pour les faces trouvées
    @return faces: "list" des faces trouvées [[(x1,y1,z1),(x2,y2,z2),(x3,y3,z3)],...,[(xn,yn,zn),(xn+1,yn+1,zn+1),(xn+2,yn+2,zn+2)]]
    """
    if (fileformat == 'b'):
      
      _file = open(self._filename, "rb")
    
      #80 Any text such as the  global g_working_dir
      #creator's name
      _header = unpack("<80s", _file.read(80))
    
      #4 int equal to the number of facets in file
      facets = unpack("i", _file.read(4))
    
      #4 vertice data in the rest of the data excapt last 2 bytes
      # Collect vert data from RAW format
      faces = []
      for _i in range(0, facets[0]):
        _n_x = unpack("f", _file.read(4))
        _n_y = unpack("f", _file.read(4))
        _n_z = unpack("f", _file.read(4))
        v1_x = unpack("f", _file.read(4))
        v1_y = unpack("f", _file.read(4))
        v1_z = unpack("f", _file.read(4))
        v2_x = unpack("f", _file.read(4))
        v2_y = unpack("f", _file.read(4))
        v2_z = unpack("f", _file.read(4))
        v3_x = unpack("f", _file.read(4))
        v3_y = unpack("f", _file.read(4))
        v3_z = unpack("f", _file.read(4))
        unused = _file.read(2)
      
        faces.append([(v1_x[0]*scale, v1_y[0]*scale, v1_z[0]*scale), (v2_x[0]*scale, v2_y[0]*scale, v2_z[0]*scale), (v3_x[0]*scale, v3_y[0]*scale, v3_z[0]*scale)])
      
      _file.close()
    
    else:
      
      _file = open(self._filename, "r")
    
      faces = []
    
      v = 0
  
      for line in _file.readlines():
        line = line.lstrip()
        if line.find("facet") == 0:
          v = 0
          #print "facet "
          normal = line.split()[-3:]
          _n_x = float(normal[0])
          _n_y = float(normal[1])
          _n_z = float(normal[2])
          #print "normal " #+ n_x + " " + n_y + " " + n_z
          continue
      
        if line.find("vertex") == 0:
          v = v + 1
      
          if v == 1:
            vertex = line.split()[-3:]
            v1_x = float(vertex[0])
            v1_y = float(vertex[1])
            v1_z = float(vertex[2])
            #print "vertex1 " #+ " " + v1_x + " " + v1_y + " " + v1_z
        
          if v == 2:
            vertex = line.split()[-3:]
            v2_x = float(vertex[0])
            v2_y = float(vertex[1])
            v2_z = float(vertex[2])
            #print "vertex2 " #+ v2_x + " " + v2_y + " " + v2_z
        
          if v == 3:
            vertex = line.split()[-3:]
            v3_x = float(vertex[0])
            v3_y = float(vertex[1])
            v3_z = float(vertex[2])
            #print "vertex3 " #+ v3_x + " " + v3_y + " " + v3_z
  
        if v == 3:
          faces.append([(v1_x*scale, v1_y*scale, v1_z*scale), (v2_x*scale, v2_y*scale, v2_z*scale), (v3_x*scale, v3_y*scale, v3_z*scale)])
  
      _file.close()
    
    return(faces)