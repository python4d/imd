#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 27 nov. 2012

@author: python4D


'''

# Nous utilisons le package pyvtk : http://code.google.com/p/pyvtk/
# Ce package a été modifié (débuggé) et mis en sous-package d'IMD3D
import IMD3D.pyvtk as vtk

#===============================================================================
# def get_tri_from_obj(filein,iNbNoeuds=0,queue=0):
#  """
#  Récupère les triangles d'un obj
#  @return: points=[[[x00,y00,z00],[x01,y01,z01],[x02,y02,z02]],[[x10,y10,z10],[x11,y11,z11],[x12,y12,z12]]]
#  @return: cell_data={} pour compatibilité avec la fonction get_quad_from_vtk
#  """
#  assert filein[-3:]=="obj"
#  vertices=[]
#  faces=[]
#  points=[]
#  cell_data={}
#  fi=open(filein,"r")
#  for i in fi.readlines():
#    try: #les lignes vides "\n" font planter le split...
#      if i.split()[0]=="v":
#        vertices.append([float(i.split()[1]),float(i.split()[2]),float(i.split()[3])])
#      if i.split()[0]=="f":
#        faces.append([int(i.split()[1]),int(i.split()[2]),int(i.split()[3])])
#    except:
#      pass
#  for f in faces:
#    points.append([vertices[f[0]-1],vertices[f[1]-1],vertices[f[2]-1]])
#  if not queue==0:
#    queue.put([[points,cell_data],0,filein])#ne vient pas du cache
#  return points,cell_data
#===============================================================================

def get_from_obj(filein,iNbNoeuds=0,queue=0):  
  """
  Récupère les quad et triangles d'un obj et normales si elles existent. PAS DE TEXTURE RECUPERE  (cf http://en.wikipedia.org/wiki/Wavefront_.obj_file)
  @return: points=[[[x00,y00,z00],[x01,y01,z01],[x02,y02,z02]],[[x10,y10,z10],[x11,y11,z11],[x12,y12,z12]]]
  @return: cell_data={} pour compatibilité avec la fonction get_quad_from_vtk
  """
  numVerts = 0
  verts = []
  norms = []
  vertsOut = []
  normsOut = []
  points=[]
  normals=[]
  cell_data={}
  for line in open(filein, "r"):
    vals = line.split()
    if vals[0] == "v":
      v = map(float, vals[1:4])
      verts.append(v)
    if vals[0] == "vn":
      n = map(float, vals[1:4])
      norms.append(n)
    if vals[0] == "f":
      for f in vals[1:]:
        w = f.split("/")
        # OBJ Files are 1-indexed so we must subtract 1 below
        vertsOut.append(list(verts[int(w[0])-1]))
        if len(w)==2:
          normsOut.append(list(norms[int(w[2])-1]))
        numVerts += 1
      points.append(vertsOut)
      normals.append(normsOut)
      vertsOut = []
      normsOut = []
  if not queue==0:
    queue.put([[points,cell_data],0,filein])#ne vient pas du cache
  return points, cell_data

def get_quad_from_vtk(filein,iNbNoeuds=0,queue=0):
  """
  Récupère les données d'un fichier (filein) vtk, avec un nb de noeud spécifié (si iNbNoeuds=0 on prends tous les Noeuds)
   et éventuellement une queue:
  la queue est utiliser pour permettre de lancer cette fonction en thread
  VisuOpenGL vérifie si cette queue est vide ou non avant de dessiner les points
  'permet de ne pas figé le programme pendant le parsing du fichier vtk)
   et évntuellement un cache:
  Le cache permet de mettre dans un DICT les points avec l'étiquette 'filein' (utilisé au moment de la sélection dan sla liste VTK)
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
  Créer deux fichiers obj avec les données vtk (récupérer via le package pyvtk)
  filein.vtk est un fichier venant ABSOLUMENT de PLAST
  fileout.obj est un fichier 3D qui récupère uniquement les iNbNoeuds-ième premier POINTS et les correspondant QUAD du fichier filein
  fileout_tri.obj est une version fileout.obj avec des faces tri plutôt que quad indispensable pour ANNA.
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
  
  
