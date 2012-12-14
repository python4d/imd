#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 31 d�c. 2012
D�finition de la Class Projet permettant de cr�er l'ensemble de actions li�es au projet.
-Gestion Nouveau, Ouvrir et Enregistrer Projet (cr�ation de l'espace projet � l'enregistrement) 
-Gestion de l'IHM suivant less informations projet 
-Gestion des conversions Projet => .DAT Plast
@author: Python4D
'''
import os,wx
from IMD3D import __version__

class ProjetIMD(object):
  """
  Permet de cr�er un objet qui regroupe l'ensemble des informations permettant de lancer PLAST
  et ANNA (param�tres IHM et liste des fichiers) et capable de cr�er une structure
  de type r�pertoire-projet avec l'ensemble de ces fichiers entr�es et sortie des deux ex�cutable.
  """
  wildcard="IMD Projet (*.imd)|*.imd"
  def __init__(self,frame):
    self.frame=frame
    self.save=1 #flag pour savoir si le projet a �t� sauvegard�
    self.projet=self._ProjetVide()
    self.Projet2IHM(self.projet,self.frame)
    
  def _ProjetVide(self):
    """
    Cr�e un projet vide renvoie un dict avec le minimum d'info
    Structure des donn�es minimum du JSON
    """  
    projet={}
    projet["Version des fichiers projet"]=__version__
    projet["root"]={}
    projet["root"]["Nom du Projet"]="*sans titre"
    projet["root"]["Dossier du Projet"]=".sans titre"
    projet["root"]["dir"]={}
    projet["root"]["dir"]["plast3d"]=r".\plast3d"
    projet["root"]["dir"]["anna"]=r""
    projet["root"]["fichier STL moule"]=r""
    projet["root"]["fichier STL film"]=r""
    projet["root"]["fichier thermique.dat"]=r""
    projet["root"]["fichier vitesse.dat"]=r""
    projet["root"]["fichier plast.dat"]=r""
    #cr�ation du directory projet o� sont import�s tous les fichier .dat, stl, vtk, obj, materiau
    try:
      os.rmdir(projet["root"]["Dossier du Projet"])
    except:
      pass
    os.mkdir(projet["root"]["Dossier du Projet"])
    return(projet)
  
  def Projet2IHM(self,projet,frame):
    frame.Title=frame.Title.split(' - ')[0]+" - "+projet["root"]["Nom du Projet"]
    #directory plast
    frame.m_dirPicker_PLAST3D.SetPath(projet["root"]["dir"]["plast3d"])
    frame.m_menuItem_Projet_Save.Enable(self.save)
    
  def OnMenuSelection_Projet_New(self, event):
    if self.projet["root"]["Nom du Projet"][0]=="*":
    #Demande si l'on veut sauvegarder le fichier en cours avant de cr�er un nouveau fichier
      _dlg=wx.MessageDialog(parent=None, message="Voulez-vous Sauvegarder les donn�es projets ?",  caption="Sauvegarde", style=wx.OK|wx.CANCEL|wx.ICON_QUESTION)
      if _dlg.ShowModal()==wx.ID_OK:
        self._DialogSaveFile()
      else:
        pass
      _dlg.Destroy()
      self.projet=self._ProjetVide()
      self.Projet2IHM(self.projet,self.frame)





  def _DialogSaveFile(self):
    """
    Create and show the Save FileDialog
    """
    _dlg = wx.FileDialog(self.frame, message="Enregistrer le fichier projet sous ...", 
                        defaultDir=self.projet["root"]["Dossier du Projet"]+r"\..", 
                        defaultFile="", wildcard=ProjetIMD.wildcard, style=wx.SAVE)
    if _dlg.ShowModal() == wx.ID_OK:
      _path = _dlg.GetPath()
      print "You chose the following filename: %s" % _path
      return _path
    else:
      return -1
    _dlg.Destroy()
      
  def _DialogOpenFile(self):
    """
    Create and show the Open FileDialog
    """
    _dlg = wx.FileDialog(self.frame, message="Choisir un projet IMD",
                        defaultDir=self.currentDirectory, 
                        defaultFile="",
                        wildcard=ProjetIMD.wildcard,
                        style=wx.OPEN |  wx.CHANGE_DIR)
    if _dlg.ShowModal() == wx.ID_OK:
      _path = _dlg.GetPaths()
      print "You chose the following file(s):", _path
      return _path
    else:
      return -1
    _dlg.Destroy()    
    
    
    
"""    
    import json
    jj=json.dumps(project,indent=4, separators=(',', ': '),encoding="utf-8")
    with open("toto.json",mode="w") as f:
      f.write(jj)
    with open("toto.json","r") as g:
      gg=g.read()
    print gg
    jj=json.loads(gg,encoding="utf-8")
    print jj
"""    