#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 2 déc. 2012
Regroupe toutes les fonctions concernant le Panel NoteBook
Ne sert que pour alléger le fichier MainApp
@author: Python4D
'''
import Common
import wx
import vtk2obj


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
   
  _filein=str(event.String.split(" -> ")[1])
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
    self.m_listBox_vtk.Set([a.split('\\')[-1]+" -> "+a for a in list_fichiers_vtk])
    self.cache_liste_points={}
    return 0
  else:
    return -1

#  
# Fonctions concernant l'onglet données du projet (parametres/valeurs)
#
def OnDirChanged_PLAST3D( self, event ):
  _dir=self.m_dirPicker_PLAST3D.GetPath()
  if not self.m_dirPicker_PLAST3D.CheckPath(_dir): #a priori le test n'est pas nécessaire puisque l'on a mis le check automatique dans l'IHM DirPicker
      dlg = wx.MessageDialog(None, "Directory inexistant!" ,"Warning dans OnDirChanged_PLAST3D!",wx.OK|wx.ICON_INFORMATION)
      dlg.ShowModal()
      dlg.Destroy() 
      self.m_dirPicker_PLAST3D.SetPath(self.old_dir_Plast3D)                
  event.Skip()
  
def OnKillFocus_DIR_PLAST3D(self, event):
  print "KillFocus-event OnChangeText_DIR_PLAST3D \n"
  _dir=self.m_dirPicker_PLAST3D.GetTextCtrl().GetValue()
  self.m_dirPicker_PLAST3D.SetPath(_dir) 
  if  RefreshOnListBox_vtk(self,_dir)==-1 :
    dlg = wx.MessageDialog(None, "Répertoire sans vtk !" ,"Warning dans OnKillFocus_DIR_PLAST3D",wx.OK|wx.ICON_INFORMATION)
    dlg.ShowModal()
    dlg.Destroy() 
    self.m_dirPicker_PLAST3D.SetPath(self.old_dir_Plast3D)   
  event.Skip()  
def OnSetFocus_DIR_PLAST3D( self, event ):
  print "SetFocus-event OnChangeText_DIR_PLAST3D \n"
  self.old_dir_Plast3D=self.m_dirPicker_PLAST3D.GetTextCtrl().GetValue()
  event.Skip()       

#
#  Fonctions concernant les wxSlider de l'onglet visualisation vtk
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

    
  
#
#  Fonctions concernant la wxSlider de l'onglet visualisation vtk
#  
def OnChoice_vtk_color(self, event):
  self.oVueOpenGL.TableCouleur=self.m_choice_vtk_color.GetStringSelection()
  self.oVueOpenGL.mCacheColor()
  self.oVueOpenGL.flag_color_change=1 #permet de recréer la Display_List (cf VisuOpenGL)
  self.oVueOpenGL.Refresh(True)
  event.Skip()

