#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Crée le 4 déc. 2012
Regroupe toutes les fonctions de traitement en dehors de l'IHM
Toutes ces fonctions sont "a priori" indépendants de l'IHM
@author: Python4D/damien
'''

import os


            

def ListVtkFiles(chemin=r".",seek_level=2):
  """
  Retourne Tous les fichiers VTK du dossier et sous dossier de niveau seek_level  désigné par chemin.
  @param seek_level: seek_level niveau des sous dossier à explorer
  @param chemin: Chemin à explorer
  """
  files_list=[]
  if os.access(chemin, os.R_OK): 
    for _r,_,_f in walklevel(chemin,seek_level):
      for files in _f:
          if files.endswith(".vtk"):
            files_list.append( os.path.join(_r,files))
    return files_list
  else:
    return -1

#Retourne le coords MEAN=[MEANX,MEANY,MEANZ] et MIN et MAX de tous les points (sommets) dans la liste des coords
def MeanMaxMin(points):
  """
  Retourne la moyenne, le max et le min d'une série de points sous la forme:
  points=[[[x0,y0,z0],[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]],[[x10,y10,z10],[x11,y11,z11],[x12,y12,z12]]]
  représente les sommets ou points des faces de l'objet (quad ou tri)
  """
  #cf http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python pour comprendre l'extraction qui suit...
  list_x=[item[0] for sublist in points for item in sublist]
  list_y=[item[1] for sublist in points for item in sublist]
  list_z=[item[2] for sublist in points for item in sublist]
  taille=len(list_x)
  _mean=[sum(list_x)/taille,sum(list_y)/taille,sum(list_z)/taille]
  _max=[max(list_x),max(list_y),max(list_z)]
  _min=[min(list_x),min(list_y),min(list_z)]    
  return _mean,_max,_min


def RotateList(l,n):
  """
  Rotation d'une liste utiliser entre autre pour changer de couleur (VisuOpenGL)
  @param l: list
  @param n: nombre de rotation, peut etre positif ou négatif
  """
  return l[n:] + l[:n]
  

def walklevel(some_dir, level=1):
  """
  It works just like os.walk, but you can pass it a level parameter that indicates how deep the recursion will go.
  @see: http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below
  """
  some_dir = some_dir.rstrip(os.path.sep)
  assert os.path.isdir(some_dir)
  num_sep = some_dir.count(os.path.sep)
  for root, dirs, files in os.walk(some_dir):
      yield root, dirs, files
      num_sep_this = root.count(os.path.sep)
      if num_sep + level <= num_sep_this:
          del dirs[:]  
