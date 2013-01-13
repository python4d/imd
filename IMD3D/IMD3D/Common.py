#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Module Crée le 4 déc. 2012
Regroupe toutes les fonctions de traitement en dehors de l'IHM
Toutes ces fonctions sont "a priori" indépendants de l'IHM
@author: Python4D/damien
'''

import os,sys,wx

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

def FindCorners(points):
  """
  Trouver 4 coins/points les plus éloignés (externes) d'une liste de triangles/quadri (points)
  @param points: points=[[[x0,y0,z0],[x1,y1,z1],[x2,y2,z2],[x3,y3,z3]],[[x10,y10,z10],[x11,y11,z11],[x12,y12,z12]]]
  @return: 4 tuples
  @todo: NE PREVOIT PAS LES DOUBLONS - TOUS LES POINTS SONT DISTINCTS
  """
  #On récupère les listes de points sur le plan xy, remap de la liste des TRI ou QUAD
  list_x=[item[0] for sublist in points for item in sublist]
  list_y=[item[1] for sublist in points for item in sublist]
  import numpy as np
  arr=np.array([list_x,list_y])
  print arr
  #Recherche du coin suivant les xmin: On recherche les xmin et on prends celui qui a le ymin
  indice_xmin=np.nonzero(arr[0,:]==arr[0,:].min())[0] 
  indice_ymin_xmin=np.nonzero((arr[1,indice_xmin]==arr[1,indice_xmin].min()))[0]
  indice_xmin=indice_xmin[indice_ymin_xmin]
  print "XMIN/YMin=",indice_xmin,'\n',arr[:,indice_xmin]
  _coin1=(arr[:,indice_xmin][0][0],arr[:,indice_xmin][1][0])  
  #Recherche du coin suivant les ymin: On recherche les ymin et on prends celui qui a le xmax
  indice_ymin=np.nonzero(arr[1,:]==arr[1,:].min())[0] 
  indice_xmax_ymin=np.nonzero((arr[0,indice_ymin]==arr[0,indice_ymin].max()))[0]
  indice_ymin=indice_ymin[indice_xmax_ymin]
  print "YMIN/XMax=",indice_ymin , '\n',arr[:,indice_ymin]
  _coin2=(arr[:,indice_ymin][0][0],arr[:,indice_ymin][1][0])
  #Recherche du coin suivant les xmax: On recherche les xmax et on prends celui qui a le ymax
  indice_xmax=np.nonzero(arr[0,:]==arr[0,:].max())[0] 
  indice_xmax_ymax=np.nonzero((arr[1,indice_xmax]==arr[1,indice_xmax].max()))[0]
  indice_xmax=indice_xmax[indice_xmax_ymax]
  print "XMAX/YMax=",indice_xmax , '\n',arr[:,indice_xmax]
  _coin3=(arr[:,indice_xmax][0][0],arr[:,indice_xmax][1][0])
  #Recherche du coin suivant les ymax: On recherche les ymax et on prends celui qui a le xmin
  indice_ymax=np.nonzero(arr[1,:]==arr.max(1)[1])[0] 
  indice_ymax_xmin=np.nonzero((arr[0,indice_ymax]==arr[0,indice_ymax].min()))[0]
  indice_ymax=indice_ymax[indice_ymax_xmin]
  print "YMAX/XMin=",indice_ymax , '\n',arr[:,indice_ymax]                     
  _coin4=(arr[:,indice_ymax][0][0],arr[:,indice_ymax][1][0])
  
  return (_coin1,_coin2,_coin3,_coin4)
  
  
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
          
class RedirectOutput(object): 
  """
  Class permettant de définir l'action "write" nécessaire à l'objet sys.sdtout ou stderr
  @param kind: string comportant le stype de sortie redirigée, soit "err" ou "out"
  @param log: object ctrlText pour injecter les message dans la console IHM
  """
  def __init__(self, kind, log): 
    self.log = log 
    self.kind = kind
  def write(self, string): 
    self.log.AppendText(string) 
    #on réinjecte le message dans l'objet de base protégé sys.__stderr__ ou sys.__stdout__
    if self.kind=="err": sys.__stderr__.write(string)
    if self.kind=="out": sys.__stdout__.write(string)

def scale_bitmap(bitmap, width, height):
  """
  Resize a bitmap
  Use of wx functions
 @note: http://stackoverflow.com/questions/2504143/how-to-resize-and-draw-an-image-using-wxpython
  """
  image = wx.ImageFromBitmap(bitmap)
  image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
  result = wx.BitmapFromImage(image)
  return result          


if __name__=="__main__":
  points=[[(-1,1,0),(-1,2,0),(2,2,0),(2,1,0)],[(0,1,0),(1,1,0),(1,-1,0),(0,-1,0)],[(-1,-1,0),(-1,-2,0),(2,-2,0),(2,-1,0)]] #la lettre I
  FindCorners(points)
