#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 3 d�c. 2012
G�re tous les timer de tous les objets de l'IHM
@author: Python4D/damien
'''

import wx,time


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
    self.frame.Bind(wx.EVT_TIMER,self.oVueOpenGL_timer,self.oVueOpenGLTimer)
    self.count=0
    
  def m_statusBar_timer(self,event):
    """
    Fonction Callback du timer qui se rapporte "principalement" au rafraichissement de la barre d'�tat
    Timer lancer d�s l'initialisation (cf __init__)
    """
    self.frame.m_statusBar.SetStatusText(time.asctime())
    event.Skip()
  
  def oVueOpenGL_timer(self,event):
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
      self.count+=10
      self.frame.m_gauge_vtk.SetValue(self.count)
      if self.frame.oVueOpenGL.flag_new_set_of_points<=0:
        #on a confirmation que les donn�es on �tait consomm� par l'objet oVueOpenGL (cf VissuOpenGL)
        self.oVueOpenGLTimer.Stop()
        self.count=0
        self.frame.m_gauge_vtk.SetValue(self.count)
    event.Skip()

    
    
    
    