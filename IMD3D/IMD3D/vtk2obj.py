#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 27 nov. 2012

@author: python4D


'''

# Nous utilisons le package pyvtk : http://code.google.com/p/pyvtk/
# Ce package a �t� modifi� (d�bugg�) et mis en sous-package d'IMD3D
import IMD3D.pyvtk as vtk

def get_quad_from_vtk(filein,iNbNoeuds=0,queue=0):
  """
  R�cup�re les donn�es d'un fichier (filein) vtk, avec un nb de noeud sp�cifi� (si iNbNoeuds=0 on prends tous les Noeuds)
   et �ventuellement une queue:
  la queue est utiliser pour permettre de lancer cette fonction en thread
  VisuOpenGL v�rifie si cette queue est vide ou non avant de dessiner les points
  'permet de ne pas fig� le programme pendant le parsing du fichier vtk)
   et �vntuellement un cache:
  Le cache permet de mettre dans un DICT les points avec l'�tiquette 'filein' (utilis� au moment de la s�lection dan sla liste VTK)
  """

  v=vtk.VtkData(filein)
  points=[]
  cell_data={}
  for pts in v.structure.quad:
    if iNbNoeuds>0:
      if pts[0]<iNbNoeuds and pts[1]<iNbNoeuds and pts[2]<iNbNoeuds and pts[3]<iNbNoeuds:
        points.append([v.structure.points[pts[0]],v.structure.points[pts[1]],v.structure.points[pts[2]],v.structure.points[pts[3]]])
    else:
      points.append([v.structure.points[pts[0]],v.structure.points[pts[1]],v.structure.points[pts[2]],v.structure.points[pts[3]]])
      
  for data in v.cell_data.data:
    cell_data[data.name]=list(data.scalars)
  
  if not queue==0:
    queue.put([[points,cell_data],0,filein])#ne vient pas du cache
  
  return points,cell_data
        
def vtk2obj(filein,fileout="",iNbNoeuds=7735):
  """
  Cr�er deux fichiers obj avec les donn�es vtk (r�cup�rer via le package pyvtk)
  filein.vtk est un fichier venant ABSOLUMENT de PLAST
  fileout.obj est un fichier 3D qui r�cup�re uniquement les iNbNoeuds-i�me premier POINTS et les correspondant QUAD du fichier filein
  fileout_tri.obj est une version fileout.obj avec des faces tri plut�t que quad indispensable pour ANNA.
  """
  assert filein[-3:]=="vtk"
  if fileout=="" :
    fileout=filein[:-3]+"obj"
  else:
    assert fileout[-3:]=="obj"
      
  v=vtk.VtkData(filein)
  fo=open(fileout,"w")
  i=0
  for pts in v.structure.points:
    if i==0: #on oublie le pt d'origine (0,0,0)
      pass
    else:
      s= 'v ' + "{:f}".format(pts[0])+' '+"{:f}".format(pts[1])+' '+"{:f}".format(pts[2])
      fo.write(s+'\n')
    i+=1
    if i==iNbNoeuds and not iNbNoeuds==0:break
  for pts in v.structure.quad:
    if pts[0]<iNbNoeuds and pts[1]<iNbNoeuds and pts[2]<iNbNoeuds and pts[3]<iNbNoeuds:
      s= 'f ' + "{:d}".format(pts[0])+' '+"{:d}".format(pts[1])+' '+"{:d}".format(pts[2])+' '+"{:d}".format(pts[3])
      fo.write(s+'\n')
  fo.close()
  fo=open(fileout[:-3]+"_tri"+".obj","w")
  i=0
  for pts in v.structure.points:
    if i==0: #on oublie le pt d'origine (0,0,0)
      pass
    else:
      s= 'v ' + "{:f}".format(pts[0])+' '+"{:f}".format(pts[1])+' '+"{:f}".format(pts[2])
      fo.write(s+'\n')
    i+=1
    if i==iNbNoeuds and not iNbNoeuds==0:break
  for pts in v.structure.quad:
    if pts[0]<iNbNoeuds and pts[1]<iNbNoeuds and pts[2]<iNbNoeuds and pts[3]<iNbNoeuds:
      s= 'f ' + "{:d}".format(pts[0])+' '+"{:d}".format(pts[1])+' '+"{:d}".format(pts[3])
      fo.write(s+'\n')
      s= 'f ' + "{:d}".format(pts[1])+' '+"{:d}".format(pts[2])+' '+"{:d}".format(pts[3])
      fo.write(s+'\n')
  fo.close()