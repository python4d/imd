#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 2 déc. 2012
Regroupe toutes les fonctions concernant le Panel NoteBook
Ce module a été créé uniquement pour alléger le fichier MainApp
@author: Python4D
'''
import Common,vtk2obj,Projet
import wx,os



def OnNotebookPageChanged(self,event):
  st=self.m_notebook.GetCurrentPage().GetName()
  print st
  event.Skip()
  
#
# Fonctions concernant la wxListBox des fichiers VTK
#
def OnListBox_vtk(self, event):
  if self.debug==False:
    #cas utilisation du multiprocessing (attention pas de debug possible lance un interpréteur Python par process!!)
    from multiprocessing import Process, Queue
  else:
    #cas utilisation des thread (n'utilise qu'un interpréteur et n'utilise donc pas le cpu à plein, 
    #permet juste de lancer en parralléle des taches pour ne pas 'trop' bloqué l'IHM
    from threading import Thread as Process
   
  _filein=str(event.String.split(" from ")[1]+"\\"+event.String.split(" from ")[0])
  if (_filein in self.cache_liste_points):
    self.oVueOpenGL.q.put([self.cache_liste_points[_filein],1,"no_file"])#on prévient que les données viennent du cache
  else:  
    # On lance un Thread pour récupérer les données du nouveau fichier
    #threading.Thread(target=vtk2obj.get_quad_from_vtk, args=(_filein,7735,self.oVueOpenGL.q,self.cache_liste_points)).start()
    Process(target=vtk2obj.get_quad_from_vtk, args=(_filein,0,self.oVueOpenGL.q)).start()   
  self.oVueOpenGL.flag_new_set_of_points+=1 #on augmente le compteur du nombre de set de points dans la queue (VisuOpenGL va décrémenter ce compteur)
  self.oTimer.oVueOpenGLTimer.Start(500)
  event.Skip()
  


def RefreshOnListBox_vtk(self,chemin='.'):  
  # Init ListBox_vtk
  list_fichiers_vtk=Common.ListVtkFiles(chemin)
  if not list_fichiers_vtk==-1:
    self.m_listBox_vtk.Set([a.split('\\')[-1]+" from "+"\\".join(a.split('\\')[:-1]) for a in list_fichiers_vtk])
    self.cache_liste_points={}
    return 0
  else:
    return -1

#  
# Fonctions concernant l'onglet données du projet (parametres/valeurs)
#
def OnDirChanged_PLAST3D( self, event ):
  if not self.m_dirPicker_PLAST3D.GetTextCtrl().FindFocus()==self.m_dirPicker_PLAST3D.GetTextCtrl():
    #cas où l'on a changé le directory via le bouton et non pas en tapant directement le chemin
    OnKillFocus_DIR_PLAST3D(self, event)
  event.Skip()
  
def OnKillFocus_DIR_PLAST3D(self, event):
  print "KillFocus-event OnChangeText_DIR_PLAST3D \n"
  _dir=self.m_dirPicker_PLAST3D.GetTextCtrl().GetValue()
  _plast3d=os.path.join(_dir,"plast3d.exe")
  if not self.oProjetIMD.ValiderDirFile(_plast3d)==0:
    self.m_dirPicker_PLAST3D.SetPath(self.oProjetIMD.projet["root"]["dir"]["plast3d"])   
  else:    
    self.m_dirPicker_PLAST3D.SetPath(_dir) 
    self.oProjetIMD.projet["root"]["dir"]["plast3d"]=_dir
    self.oProjetIMD.not_saved=1
    self.oProjetIMD.Projet2IHM(self.oProjetIMD.projet,self.oProjetIMD.frame)
    RefreshOnListBox_vtk(self,_dir)
  event.Skip()  

def OnSetFocus_DIR_PLAST3D( self, event ):
  print "SetFocus-event OnChangeText_DIR_PLAST3D \n"
  event.Skip()       

#
#  Fonctions concernant les wxSlider, choix couleur et reset view de l'onglet visualisation vtk
#
def OnScroll_slider_vtk( self, event ):      
  self.oVueOpenGL.flag_color_change=1
  self.oVueOpenGL.Refresh(True)
  event.Skip()
def OnButtonClick_vtk( self, event ):
  self.oVueOpenGL.flag_reset_view=1
  self.oVueOpenGL.Refresh(True)  
  event.Skip()
def OnScroll_slider_vtk_color( self, event ):      
  self.oVueOpenGL.flag_color_change=1
  self.oVueOpenGL.Refresh(True)
  event.Skip()
def OnChoice_vtk_color(self, event):
  self.oVueOpenGL.TableCouleur=self.m_choice_vtk_color.GetStringSelection()
  self.oVueOpenGL.mCacheColor()
  self.oVueOpenGL.flag_color_change=1 #permet de recréer la Display_List (cf VisuOpenGL)
  self.oVueOpenGL.Refresh(True)
  event.Skip()

#
#  Fonctions concernant le wxSlider et choix texture de l'onglet visualisation vtk
#
def OnChoice_texture( self, event ):
  self.oVueOpenGL.flag_texture_change=2 
  self.oVueOpenGL.Refresh(True)
  event.Skip()

     
def OnScroll_slider_texture( self, event ):
  self.oVueOpenGL.flag_texture_change=3
  self.oVueOpenGL.Refresh(True)
  event.Skip()  
  
def OnCheckBox_texture( self, event ):
  if self.m_checkBox_texture.GetValue():
    self.oVueOpenGL.flag_texture_change=1
  else:
    self.oVueOpenGL.flag_texture_change=-1
  self.oVueOpenGL.Refresh(True)
  event.Skip()


#
# Fonction concernant les splitters
#
def OnSplitterChanging(self,event):
  """
  Redessine le Frame car il semble que le Splitter ne le demande pas (tout le temps??)
  """
  self.Refresh(True)
  event.Skip()
