#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 3 d�c. 2012
G�re tous les timer de tous les objets de l'IHM
@author: Python4D/damien
'''

import wx,time
import logging
logging.basicConfig()

class cTimer(object):
  """
  cTimer n'est pas un Timer mais une class qui regroupe des Timers
  Tous ces Timers sont associ�s (bind) � la class Frame de l'IHM
  Toutes les fonctions callback des timers sont regroup� dans cette class cTimer
  (cr�er diff�rents timer et call back permet uniquement de rendre lisible le code)
  """
  def __init__(self,frame):
    self.frame=frame
    self.oStatusBarTimer=wx.Timer(frame)
    self.frame.Bind(wx.EVT_TIMER,self.m_statusBar_timer,self.oStatusBarTimer)
    self.oStatusBarTimer.Start(1000)
    self.oVueOpenGLTimer=wx.Timer(frame)
    self.frame.Bind(wx.EVT_TIMER,self.mVueOpenGLTimer,self.oVueOpenGLTimer)
    self.count=0
    self.oMessageLogTimer=wx.Timer(frame)
    self.frame.Bind(wx.EVT_TIMER,self.mMessageLogTimer,self.oMessageLogTimer)    
    self.couleur=0
    self.oRefreshListeofVTKTimer=wx.Timer(frame)
    self.frame.Bind(wx.EVT_TIMER,self.mRefreshListeofVTKTimer,self.oRefreshListeofVTKTimer)       
    self.oRefreshListeofVTKTimer.Start(60000)
         
  def m_statusBar_timer(self,event):
    """
    Fonction Callback du timer qui se rapporte "principalement" au rafraichissement de la barre d'�tat
    Timer lancer d�s l'initialisation (cf __init__)
    """
    self.frame.m_statusBar.SetStatusText(time.asctime(),0)
    event.Skip()
    
  def mRefreshListeofVTKTimer(self,event):
    """
    Fonction permettant de rafraichir constament la liste des fichiers dans la visualisation VTK
    Timer lancer � l'initialisation de MainApp uniquement si le directory plast existe
    """
    self.frame.oNoteBook.RefreshOnListBox_vtk(self.frame.oProjetIMD.projet["root"]["dir"]["plast3d"])
    event.Skip()
    
  def mVueOpenGLTimer(self,event):
    """
    Fonction Callback du timer qui se rapporte "principalement" � la VueOpenGL (onglet VTK)
    Timer lancer au moment de la s�lection d'un fichier VTK dans la ListeBox_vtk cf Module NoteBook/OnListBox_vtk
    """ 
    if not self.frame.oVueOpenGL.q.empty():
      #cas o� il reste des infos (points et cell_data vtk) dans la queue
      self.count=0
      self.frame.m_gauge_vtk.SetValue(self.count)
      self.frame.oVueOpenGL.Refresh(True) 
    else: 
      #cas o� le timer est d�marrer (donc il y eu s�lection d'un fichier VTK dans la liste)
      # mais il n'y a pas encore de donn�es dans la queue
      self.count+=5
      self.frame.m_gauge_vtk.SetValue(self.count)
      if self.count==100: self.count=0
      if self.frame.oVueOpenGL.flag_new_set_of_points<=0:
        #on a confirmation que les donn�es on �tait consomm� par l'objet oVueOpenGL (cf VissuOpenGL)
        self.oVueOpenGLTimer.Stop()
        self.count=0
        self.frame.m_gauge_vtk.SetValue(self.count)
    event.Skip()

  def mMessageLogTimer(self,event):
    """
    Timer pour la gestion visuel de la fenetre LOG: effet dynamique rouge => blanc
    TODO: pas tr�s lisible et surtout impossible de g�rer le fond des caract�res... pour l'instant abandonn�
    """
    if self.couleur==0:
      pass
    if self.couleur<255:
      self.frame.m_textCtrl_console.SetBackgroundColour(wx.Colour(255,self.couleur,self.couleur))  
      self.couleur+=10
    else:
      self.couleur=0
      self.frame.m_textCtrl_console.SetBackgroundColour(wx.Colour(255,255,255))
      self.oMessageLogTimer.Stop()
    
    
    