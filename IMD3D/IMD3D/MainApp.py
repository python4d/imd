#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 27 nov. 2012

@author: python4D
@summary: Module principal pour la création du l'application et de la fenetre (frame) principale
@version: see __version__

'''
####################################################################################################################
# pour récupérer les les infos OpenGL mis "à la main" dans dist (py2exe) cf http://www.py2exe.org/index.cgi/PyOpenGL
import sys
sys.path += ['.']
####################################################################################################################
import wx,time
from wx.lib.intctrl import IntCtrl
from IMD3D_IHM import wxMainFrame
import NoteBook
import Timer
import Projet,Common
import pystl

__version__='1.0A'


class cMainFrame(wxMainFrame):
  def __init__(self,parent=None,debug=True):
    super(cMainFrame,self).__init__(parent)

    self.debug=debug
  # Gestion des paramêtres projet
    self.oProjetIMD=Projet.ProjetIMD(self)
  # Initialiser les différents Timer
    self.oTimer=Timer.cTimer(self)

  #Initialisation des éléments IHM
    if (NoteBook.RefreshOnListBox_vtk(self,self.oProjetIMD.projet["root"]["dir"]["plast3d"])==-1):
      print >>sys.stderr,"Erreur: Répertoire ""vtk"" de base non présent sous le dossier IMD3D."
  #Init Visualisation 3D-vtk du cache des points et cell_data
    self.cache_liste_points={}
    self.m_choice_vtk_color.Clear()
    self.m_choice_vtk_color.Append("Z-Hauteur")
    self.m_choice_vtk_color.SetSelection(0)
  #test
    a=pystl.cSTL("ship.stl")
    a.read(scale=500,fileformat='b')
    _size,_buffer=a.raw_bitmap()
    image_bmp = Common.scale_bitmap(wx.BitmapFromBuffer(_size[0],_size[1],_buffer),500,500)
    self.TopLevelParent.m_bitmap_test.SetBitmap(image_bmp)
    
  #Init du directory PLAST3D-VTK (certaines propriétés IHM de la Class DirPicker ne sont pas settable via wxFormBuilder
    self.m_dirPicker_PLAST3D.SetPath(self.oProjetIMD.projet["root"]["dir"]["plast3d"])
    self.m_dirPicker_PLAST3D.GetPickerCtrl().SetLabel("Plast3D Rep.")
    #il est impossible de modifier le control text en READ_ONLY après sa création => self.m_dirPicker_PLAST3D.GetTextCtrl().SetDefaultStyle(wx.TE_READONLY)
    #On opte pour attacher l'événement KILL_FOCUS et SET_FOCUS afi de vérifier si le directory entré "à la main" est juste
    self.m_dirPicker_PLAST3D.GetTextCtrl().Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus_DIR_PLAST3D )
    self.m_dirPicker_PLAST3D.GetTextCtrl().Bind( wx.EVT_SET_FOCUS, self.OnSetFocus_DIR_PLAST3D )
  #Message dans la console
    self.m_textCtrl_console.AppendText("(c) Dynamic3D/Python4D - 01/2013 - Version %s"%__version__)
    if self.debug==True:
      self.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.RED))
      self.m_textCtrl_console.AppendText("\n(!!!Attention vous êtes en MODE Debug les chargements des fichiers et animations ne sont pas optimisés !!!)")
      self.m_textCtrl_console.SetDefaultStyle(wx.TextAttr(wx.BLACK))
    self.m_textCtrl_console.AppendText("\nBienvenue sur l'interface OpenGL/Python du projet IMD3D\n")
    if self.debug==True:
      sys.stdout = Common.RedirectOutput("out",self.m_textCtrl_console)
    sys.stderr = Common.RedirectOutput("err",self.m_textCtrl_console) 
    self.Show() 
    wx.SplashScreen(wx.Bitmap("./images/splash.png"), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT,2000, None, -1,style=wx.BORDER_NONE).Show()
  
  
  def OnClose_Frame( self, event ): 
    wx.SplashScreen(wx.Bitmap("./images/splash.png"), wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT,2000, None, -1,style=wx.BORDER_NONE).Show()
    event.Skip()
      

  def OnSplitterChanging(self,event):NoteBook.OnSplitterChanging(self,event)
    
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
  def OnMenuSelection_Projet_SaveAs(self, event):self.oProjetIMD.OnMenuSelection_Projet_Save(event,True)
  def OnMenuSelection_Projet_Save(self, event):self.oProjetIMD.OnMenuSelection_Projet_Save(event,False)
    
class cMainApp(wx.App):
  def __init__(self,debug=True):
    wx.App.__init__(self,redirect=False)
    self.oMainFrame=cMainFrame(debug=debug)
    favicon = wx.Icon('images/icons/py4d.ico', wx.BITMAP_TYPE_ICO)
    wx.Frame.SetIcon(self.oMainFrame, favicon)



from multiprocessing import Process, freeze_support
class cIMD3D(object):
  """
  Class de base de l'application IMD3D
  @param debug: si "False" permet de lancer de lancer des process child (utilisez dans Notebook)
                si "True" n'utilise qu'un process principal et des threads
  @note: Explication de l'utilisation du multiprocessing sous python - http://docs.python.org/2/library/multiprocessing.html#multiprocessing.freeze_support
  @note: Limitation dans le debug avec Pydev si debug="False" - http://stackoverflow.com/questions/6724149/python-how-to-debug-multiprocess-using-eclipsepydev
  """
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
      