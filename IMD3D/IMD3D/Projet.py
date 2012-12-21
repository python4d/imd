#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 31 déc. 2012
Définition de la Class Projet permettant de créer l'ensemble de actions liées au projet.
-Gestion Nouveau, Ouvrir et Enregistrer Projet (création de l'espace projet à l'enregistrement) 
-Gestion de l'IHM suivant less informations projet 
-Gestion des conversions Projet => .DAT Plast
@author: Python4D
'''
import os,shutil,wx
import json
from IMD3D import __version__

class ProjetIMD(object):
  """
  Permet de créer un objet qui regroupe l'ensemble des informations permettant de lancer PLAST
  et ANNA (paramêtres IHM et liste des fichiers) et capable de créer une structure
  de type répertoire-projet avec l'ensemble de ces fichiers entrées et sortie des deux exécutable.
  """
  wildcard="IMD Projet (*.imd)|*.imd"
  def __init__(self,frame):
    self.frame=frame
    self.projet=self._ProjetVide()
    self.ProjetPath=os.getcwdu()
    self.Projet2IHM(self.projet,self.frame)

    
  def _ProjetVide(self):
    """
    Crée un projet vide renvoie un dict avec le minimum d'info
    Structure des données minimum du JSON
    """  
    self.not_saved=1 #flag pour savoir si le projet a été sauvegardé
    projet={}
    projet["Version des fichiers projet"]=__version__
    projet["root"]={}
    projet["root"]["Nom du Projet"]="sans titre"
    projet["root"]["Dossier du Projet"]=".sans titre"
    projet["root"]["dir"]={}
    projet["root"]["dir"]["plast3d"]=r".\plast3d"
    projet["root"]["dir"]["anna"]=r""
    projet["root"]["fichier STL moule"]=r""
    projet["root"]["fichier STL film"]=r""
    projet["root"]["fichier thermique.dat"]=r""
    projet["root"]["fichier vitesse.dat"]=r""
    projet["root"]["fichier plast.dat"]=r""
    #création du directory projet où sont importés tous les fichier .dat, stl, vtk, obj, materiau
    try:
      os.rmdir(projet["root"]["Dossier du Projet"])
    except:
      pass
    os.mkdir(projet["root"]["Dossier du Projet"])
    return(projet)
  
  def Projet2IHM(self,projet,frame):
    _ns='*' if self.not_saved==1 else ''
    frame.Title=frame.Title.split(' - ')[0]+" - "+_ns+self.ProjetPath+"\\"+projet["root"]["Nom du Projet"]
    frame.m_menuItem_Projet_Save.Enable(self.not_saved)
    #directory plast
    frame.m_dirPicker_PLAST3D.SetPath(projet["root"]["dir"]["plast3d"])

    
    

  def OnMenuSelection_Projet_New(self, event):
    """
    Créer un nouveau projet: nouveaux paramêtres, nouveau dossier fichiers, etc...
    Vérifier que ce projet a été précédemment sauvegardé
    """
    _flag=1
    if self.not_saved:
      _flag=0
    #Demande si l'on veut sauvegarder le fichier en cours avant de créer un nouveau fichier
      _dlg=wx.MessageDialog(parent=None, message="Voulez-vous Sauvegarder les données projets ?",  caption="Sauvegarde", style=wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
      _reponse=_dlg.ShowModal()
      
      if _reponse==wx.ID_YES:
        if not self.OnMenuSelection_Projet_Save(event)==-1:
          _flag=1

      elif _reponse==wx.ID_NO:
        _flag=1
        
      _dlg.Destroy()
      
    if _flag==1:
      self.projet=self._ProjetVide()
      self.Projet2IHM(self.projet,self.frame)


  def OnMenuSelection_Projet_Save(self, event,saveas):

    if self.projet["root"]["Nom du Projet"]=="sans titre" or saveas:    
      _path=self._DialogSaveFile()
      
      while not _path==-1:
        try :
          with open(_path) as _f: 
            _dlg = wx.MessageDialog(None, "Le Fichier/Dossier Projet %s existe déjà ! \nVoulez-vous l'écraser?" % _path.split('\x5C')[-1] ,"Warning dans OnMenuSelection_Projet_Save", style=wx.YES_NO|wx.CANCEL|wx.ICON_QUESTION)
            _reponse=_dlg.ShowModal()
            
            if _reponse==wx.ID_YES:
              break

            elif _reponse==wx.ID_NO:
              _dlg.Destroy()               
              _path=self._DialogSaveFile()
              
            elif _reponse==wx.ID_CANCEL:
              _dlg.Destroy() 
              return -1
            
        except IOError as _e:
          break
    else:
      _path=self.ProjetPath+"\\"+self.projet["root"]["Nom du Projet"]
    self._SaveProject(_path,self.projet)
    self.not_saved=0
    self.Projet2IHM(self.projet, self.frame)
    return 0




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
    
    
  def ValiderDirFile(self,value):
    """
    Vérifie la présence d'un fichier
    @param value: directory+fichier à vérifier
    @note: http://stackoverflow.com/questions/82831/how-do-i-check-if-a-file-exists-using-python
    """
    try :
      with open(value) as _f: pass
      return 0
    except IOError as _e:
      dlg = wx.MessageDialog(None, "Répertoire non valide sans %s !" % value.split('\x5C')[-1] ,"Warning dans OnKillFocus_DIR_PLAST3D",wx.OK|wx.ICON_INFORMATION)
      dlg.ShowModal()
      dlg.Destroy() 
      return -1
    
    
  def _LoadProject(self,name,projet):
    with open("toto.json","r") as g:
      gg=g.read()
    print gg
    jj=json.loads(gg,encoding="utf-8")
    print jj
    
  def _SaveProject(self,fullname,projet):
    """
    Sauvegarde sous la forme JSON ASCII les donnée projet (dict)
    @param fullname: nom du fichier avec son chemin
    @param projet: projet (type dict)
    """
    self.projet["root"]["Nom du Projet"]=fullname.split('\x5C')[-1]
    self.projet["root"]["Dossier du Projet"]="."+fullname.split('\x5C')[-1] 
    _p,_=os.path.split(fullname)
    try:
      shutil.rmtree(os.path.join(_p,self.projet["root"]["Dossier du Projet"]))
    except:
      print "Error à la destruction du dossier %s ." % os.path.join(_p,self.projet["root"]["Dossier du Projet"])
    os.mkdir(os.path.join(_p,self.projet["root"]["Dossier du Projet"]))

    _p=json.dumps(projet,indent=4, separators=(',', ': '),encoding="utf-8")
    with open(fullname,mode="w") as f:
      f.write(_p)
    
    
"""    



"""    