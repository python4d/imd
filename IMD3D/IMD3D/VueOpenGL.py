#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 3 D�c. 2012

@author: damien
'''

import colorsys
from multiprocessing import Queue
import Common
try:
    from OpenGL.platform import win32
except AttributeError:
    pass
import math
import logging
logging.basicConfig()
import wx.glcanvas
try:
    import OpenGL.GL as gl
    import OpenGL.GLU as glu
except ImportError:
    raise ImportError, "Required dependency OpenGL not present"
  
class cCamera(object):
  def __init__(self,r=100,theta=0.44,phi=0.61,eye_view=[0.0,0.0,0.0]):
    self.r=r
    self._theta=theta
    self.senstheta=1  
    self.phi=phi
    self.eye_view=eye_view

  @property
  def theta(self):
    return self._theta
  @theta.setter
  def theta(self,value):
    self._theta=value

    
  def mSetVue(self):
      glu.gluLookAt(self.r,  0.0, 0.0,0.0, 0.0,0.0,0.0, 0.0, 1.0)
      gl.glRotated(self.theta*180/math.pi, 0.0,1.0,0.0)
      gl.glRotated(+self.phi*180/math.pi, 0.0,0.0,1.0)

    
    
class cMainVueOpenGL(wx.glcanvas.GLCanvas):
  def __init__(self, *args, **kwargs):
    wx.glcanvas.GLCanvas.__init__(self, *args, **kwargs)
    
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)#ne sert � rien uniquement pour �viter le flash sous MSW et uniquement en Python...
    self.Bind(wx.EVT_PAINT, self.mDessine)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_KEY_DOWN, self.mAppuiTouche)
    self.Bind(wx.EVT_MOUSE_EVENTS, self.mEvenementSouris)
    
    self._frame=self.TopLevelParent
    self.bd=0
    self.flag_reset_view=0
    self.flag_new_set_of_points=0
    self.x,self.y=0,0
    self.senstheta=-1
    self.init = False
    # Cr�er une queue de donn�e rempli par la fonction get_quad_from_vtk du module vtk2obj (utile si cette fonction est appel� dans un thread)
    # V�rifier qu'il n'y a rien dans la queue avant de dessiner
    self.q=Queue()
    self.points=[[(-1,1,0),(-1,2,0),(2,2,0),(2,1,0)],[(0,1,0),(1,1,0),(1,-1,0),(0,-1,0)],[(-1,-1,0),(-1,-2,0),(2,-2,0),(2,-1,0)]] #la lettre I
    self.mean,self.max,self.min=Common.MeanMaxMin(self.points)  
    self.oCamera=cCamera(eye_view=self.mean)
    # D�fini N coleurs diff�rentes matrice de transformation HSV vers RGB
    # La saturation et valeur r�glable via le Slider (utilisation d'un flag=>cf NoteBBook module)
    self.flag_color_change=0
    self.N = 512
    HSV_tuples = [(x*1.0/self.N, 0.75, 0.75) for x in range(self.N)]
    self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    # Donn�es des couleurs ou data de chaque cell (quads) - Gestion de IHM pour le choix des couleurs
    self.cell_data,self.cd_max,self.cd_min={},{},{}
    self.TableCouleur="Z-Hauteur"
    self.cache_color={}
    self.mCacheColor()

    
  def OnSize(self, event):
    size = self.size = self.GetClientSize()
    if self.GetContext() and self.GrandParent.GrandParent.GetSelection()==2 and not size[0]==0 and not size[1]==0: #v�rifie que l'on est bien dans l'onglet visualisation 3D sinon warning wx canvas
        self.SetCurrent()
        gl.glViewport(0, 0, size.width, size.height)
    event.Skip()
    
  def mInitOpenGL(self):
    #Active la gestion de la profondeur
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel (gl.GL_FLAT) #default gl.GL_SMOOTH
    # Fixe la perspective
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(65.0, 4./3., 1.0, 1000.0)
    # fixe le fond d'�cran � noir
    gl.glClearColor(0.0, 0.0, 0.0, 1.0)
    # pr�pare � travailler sur le mod�le
    # (donn�es de l'application)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    #On cr�e la display list
    self.mCreerDisplayList()
    
  def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.
   
  def mCacheColor(self):
    #Gestion de la couleur � l'avance,  appel� entre autre par NoteBook.OnChoice_vtk_color
    j=0
    self.cache_color[self.TableCouleur]=[]
    for i in self.points:
      if  not self.TableCouleur=="Z-Hauteur":
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((self.cell_data[self.TableCouleur][j]-self.cd_min[self.TableCouleur])/(self.cd_max[self.TableCouleur]-self.cd_min[self.TableCouleur]+1e-99)))-1])
      else:
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((i[0][2]-self.min[2])/(self.max[2]-self.min[2]+1e-99)))-1])  
      j+=1 
   
  
  def mCreerDisplayList(self):
    """
    Utilisation des DisplayList d'OpenGL pour mettre en cache une sc�ne statique ou un objet
    Cette Fonction est appel� � l'init OpenGL puis � chaque fois que les vertex (points) ou la couleur change
    cf http://www.siteduzero.com/tutoriel-3-3841-afficher-une-display-list.html
    """
    self.dl=gl.glGenLists(1)
    gl.glNewList(self.dl,gl.GL_COMPILE)
    ################################ Cr�ation de l'objet
    j=0
    for i in self.points:
      gl.glColor3d(*self.cache_color[self.TableCouleur][j])
      # Boucle sur les diff�rents sommet de l'�l�ment (QUAD ou TRI � afficher)
      for k in i:
        gl.glVertex3d(k[0],k[1],k[2])
      j+=1
    ################################ Cr�ation de l'objet (fin)
    gl.glEndList()
  
  def mDessine(self,event):
    """
    Fonction Principale pour dessiner la sc�ne "OpenGL"
    Cette fonction est la fonction callback de l'�v�nement PAINT [self.Bind(wx.EVT_PAINT, self.mDessine)]
    Fortement utiliser dans toutes l'Application elle est appel� indirectement via la fonction Refresh(True) de l'objet oVisuOpenGL
    ATTENTION!! Chaque Ajout dans cette fonction peut ralentir l'animation OpenGL!!!
    """
    #V�rifie qu'il n'y a rien dans la queue
    if not self.q.empty()==True:
      [self.points,self.cell_data],_flag_cache,_filein=self.q.get() #on r�cup�re les points, on r�cup�re le flag pour savoir si les points viennent du cache ou pas
      if _flag_cache==0:# si les donn�es ne viennent pas du cache il faut les mettre
        self._frame.cache_liste_points[_filein]=[self.points,self.cell_data]
      self.flag_new_set_of_points-=1
      self._frame.m_textCtrl_console.AppendText(".")
      self.mean,self.max,self.min=Common.MeanMaxMin(self.points) 
      #R�cup�ration des Map de couleur dans les cell_data, mis � jour de la liste de choix couleur
      self._frame.m_choice_vtk_color.Clear()
      self._frame.m_choice_vtk_color.Append("Z-Hauteur")
      for _i in self.cell_data:
        self.cd_max[_i],self.cd_min[_i]=min(self.cell_data[_i]),max(self.cell_data[_i])
        self._frame.m_choice_vtk_color.Append(_i)
      self._frame.m_choice_vtk_color.SetSelection(0)
      self.mCacheColor()
      self.mCreerDisplayList()
    #Cr�ation de tuple de couleur HSV
    if not self.flag_color_change==0:
      #cas de changement de saturation/couleur (cf NoteBook.OnScroll_slider_vtk) ou
      HSV_tuples = [(x*1.0/self.N, float(self._frame.m_slider_vtk.GetValue())/100.0, float(self._frame.m_slider_vtk.GetValue())/100.0) for x in range(self.N)]
      HSV_tuples = Common.RotateList(HSV_tuples, self._frame.m_slider_vtk_color.GetValue())
      self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
      self.mCacheColor()
      self.flag_color_change=0
      self.mCreerDisplayList()
      
    #Indique que les instructions OpenGL s'adressent au contexte OpenGL courant
    self.SetCurrent()
    if not self.init:
      self.mInitOpenGL()
      self.init = True

    #initialise les donn�es li�es � la gestion de la profondeur
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # initialise GL_MODELVIEW
    # place le rep�re en (0,0,0)
    gl.glLoadIdentity()

    #On positionne la cam�ra
    if self.flag_reset_view==1:
      #cas ou l'on remet la cam�ra en position "moyenne" lorsque l'on clique sur le bouton Reset View (cf NoteBook)
      self.oCamera=cCamera()
      self.flag_reset_view=0
    self.oCamera.mSetVue()
    gl.glTranslate(-self.mean[0],-self.mean[1],-self.mean[2])
    
    gl.glEnable(gl.GL_LINE_SMOOTH)    
    
    
    gl.glBegin(gl.GL_QUADS)    
    gl.glCallList(self.dl)
    gl.glEnd()
    
    #Finalement, envoi du dessin � l �cran
    gl.glFlush()
    self.SwapBuffers()
    event.Skip()
    
  def mAppuiTouche(self,event):
    e=event.GetKeyCode()
    if e==wx.WXK_LEFT:
      self.oCamera.phi-=0.1
    elif e==wx.WXK_RIGHT:
      self.oCamera.phi+=0.1
    elif e==wx.WXK_UP:
      self.oCamera.theta-=0.1
    elif e==wx.WXK_DOWN:
      self.oCamera.theta+=0.1     
    elif e==wx.WXK_NUMPAD_ADD:
      self.oCamera.r-=1         
    elif e==wx.WXK_NUMPAD_SUBTRACT:
      self.oCamera.r+=1   
      return(0)
    self.Refresh(True)
    event.Skip()
  
    
  def mEvenementSouris(self,event):
    amt = event.GetWheelRotation() 
    if abs(amt)>0:
      units = amt/(-(event.GetWheelDelta())) 
      self.oCamera.r+=units*3
      self.Refresh(True)  
    if event.ButtonDown():
      self.bd=1
      self.t0=self.oCamera.theta
      self.p0=self.oCamera.phi
    if self.bd>=1:
      (self.x0,self.y0)=event.GetPosition()
      self.oCamera.theta=(self.t0+(self.y0-self.y)/100.0)
      self.oCamera.phi=(self.p0+(self.x0-self.x)/100.0)
      if True:
        self.Refresh(True)         
    else:
      (self.x,self.y)=event.GetPosition() 
    if event.ButtonUp():
      self.bd=0 
    event.Skip()   
    
    
