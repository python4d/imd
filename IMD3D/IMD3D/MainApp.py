#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 27 nov. 2012

@author: python4D


'''
####################################################################################################################
# pour r�cup�rer les les infos OpenGL mis "� la main" dans dist (py2exe) cf http://www.py2exe.org/index.cgi/PyOpenGL
import sys
sys.path += ['.']
####################################################################################################################
import wx,time
from IMD3D_IHM import wxMainFrame
import NoteBook
import Timer
import Projet

__version__='1.0A'


class cMainFrame(wxMainFrame):
  def __init__(self,parent=None,debug=True):
    super(cMainFrame,self).__init__(parent)

    self.debug=debug
  # Gestion des param�tres projet
    self.oProjetIMD=Projet.ProjetIMD(self)
  # Initialiser les diff�rents Timer
    self.oTimer=Timer.cTimer(self)
    
  #Initialisation des �l�ments IHM
    if (NoteBook.RefreshOnListBox_vtk(self,self.oProjetIMD.projet["root"]["dir"]["plast3d"])==-1):
      print >>sys.stderr,"Erreur: R�pertoire ""vtk"" de base non pr�sent sous le dossier IMD3D."
    #Init Visualisation 3D-vtk du cache des points et cell_data
    self.cache_liste_points={}
    self.m_choice_vtk_color.Clear()
    self.m_choice_vtk_color.Append("Z-Hauteur")
    self.m_choice_vtk_color.SetSelection(0)
    
  #Init du directory PLAST3D-VTK (certaines propri�t�s IHM de la Class DirPicker ne sont pas settable via wxFormBuilder
    self.m_dirPicker_PLAST3D.SetPath(self.oProjetIMD.projet["root"]["dir"]["plast3d"])
    self.m_dirPicker_PLAST3D.GetPickerCtrl().SetLabel("Plast3D Rep.")
    #il est impossible de modifier le control text en READ_ONLY apr�s sa cr�ation => self.m_dirPicker_PLAST3D.GetTextCtrl().SetDefaultStyle(wx.TE_READONLY)
    #On opte pour attacher l'�v�nement KILL_FOCUS et SET_FOCUS afi de v�rifier si le directory entr� "� la main" est juste
    self.m_dirPicker_PLAST3D.GetTextCtrl().Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus_DIR_PLAST3D )
    self.m_dirPicker_PLAST3D.GetTextCtrl().Bind( wx.EVT_SET_FOCUS, self.OnSetFocus_DIR_PLAST3D )
    self.old_dir_Plast3D=self.oProjetIMD.projet["root"]["dir"]["plast3d"]
  #Message dans la console
    self.m_textCtrl_console.AppendText("(c) Dynamic3D/Python4D - 01/2013 - Version %s"%__version__)
    if self.debug==True:
      self.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.RED))
      self.m_textCtrl_console.AppendText("\n(!!!Attention vous �tes en MODE Debug les chargements des fichiers et animations ne sont pas optimis�s !!!)")
      self.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.BLACK))
    self.m_textCtrl_console.AppendText("\nBienvenue sur l'interface OpenGL/Python du projet IMD3D\n")
    self.Show() 
    wx.SplashScreen(wx.Bitmap("./images/image10.png"), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT,10000, None, -1,style=wx.BORDER_NONE).Show()
  def OnClose_Frame( self, event ): pass
      

    
  def OnNotebookPageChanged(self,event): NoteBook.OnNotebookPageChanged(self,event)
  def OnDirChanged_PLAST3D( self, event ): NoteBook.OnDirChanged_PLAST3D( self, event )
  def OnKillFocus_DIR_PLAST3D( self, event ): NoteBook.OnKillFocus_DIR_PLAST3D(self, event)
  def OnSetFocus_DIR_PLAST3D( self, event ): NoteBook.OnSetFocus_DIR_PLAST3D(self, event)
  
  def OnListBox_vtk( self, event ): NoteBook.OnListBox_vtk(self, event )
  def OnScroll_slider_vtk( self, event ): NoteBook.OnScroll_slider_vtk( self, event )   
  def OnScroll_slider_vtk_color( self, event ): NoteBook.OnScroll_slider_vtk_color( self, event ) 
  def OnButtonClick_vtk( self, event ):NoteBook.OnButtonClick_vtk( self, event )
  def OnChoice_vtk_color(self, event):NoteBook.OnChoice_vtk_color(self, event)
  
  def OnMenuSelection_Projet_New(self, event):self.oProjetIMD.OnMenuSelection_Projet_New(event)

class cMainApp(wx.App):
  def __init__(self,debug=True):
    wx.App.__init__(self,redirect=False)
    self.oMainFrame=cMainFrame(debug=debug)


#
#Explication de l'utilisation du multiprocessing sous python:
#http://docs.python.org/2/library/multiprocessing.html#multiprocessing.freeze_support
#
from multiprocessing import Process, freeze_support
class cIMD3D(object):
  def __init__(self,debug=True):
    self.debug=debug
    
  def f(self):
    oApplication=cMainApp(debug=self.debug)
    oApplication.MainLoop()
    
  def run(self):
    if self.debug==False:
      freeze_support()
      Process(target=self.f).start()
    else:
      self.f()
      