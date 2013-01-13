#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
'''
Created on 3 Déc. 2012

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
    import OpenGL.GLUT as glut
except ImportError:
    raise ImportError, "Required dependency OpenGL not present"
  
class cCamera(object):
  def __init__(self,r=22,theta=0.44,phi=0.61,xy=[0.0,0.0],eye_view=[0.0,0.0,0.0]):
    self.r=r
    self._theta=theta
    self.senstheta=1  
    self.phi=phi
    self.xy=xy
    self.eye_view=eye_view

  @property
  def theta(self):
    return self._theta
  @theta.setter
  def theta(self,value):
    self._theta=value

    
  def mSetVue(self):
      glu.gluLookAt(self.r,0.0,0.0,  0.0,self.xy[0],self.xy[1],  0.0, 0.0, 1.0)
      gl.glRotated(self.theta*180/math.pi, 0.0,1.0,0.0)
      gl.glRotated(+self.phi*180/math.pi, 0.0,0.0,1.0)

    
    
class cMainVueOpenGL(wx.glcanvas.GLCanvas):
  def __init__(self, *args, **kwargs):
    wx.glcanvas.GLCanvas.__init__(self, *args, **kwargs)
    
    self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)#ne sert à rien uniquement pour éviter le flash sous MSW et uniquement en Python...
    self.Bind(wx.EVT_PAINT, self.mDessine)
    self.Bind(wx.EVT_SIZE, self.OnSize)
    self.Bind(wx.EVT_KEY_DOWN, self.mAppuiTouche)
    self.Bind(wx.EVT_MOUSE_EVENTS, self.mEvenementSouris)
    
    self._frame=self.TopLevelParent
    self.lbd,self.rbd=(0,0)
    self.flag_reset_view=0
    self.flag_new_set_of_points=0
    self.x,self.y=0,0
    self.senstheta=-1
    self.init = False
    # Créer une queue de donnée rempli par la fonction get_quad_from_vtk du module vtk2obj (utile si cette fonction est appelé dans un thread)
    # Vérifier qu'il n'y a rien dans la queue avant de dessiner
    self.q=Queue()
    self.points=[[(-1,1,0),(-1,2,0),(2,2,0),(2,1,0)],[(0,1,0),(1,1,0),(1,-1,0),(0,-1,0)],[(-1,-1,0),(-1,-2,0),(2,-2,0),(2,-1,0)]] #la lettre I
    self.mean,self.max,self.min=Common.MeanMaxMin(self.points)  
    self.oCamera=cCamera(eye_view=self.mean)
    # Défini N coleurs différentes matrice de transformation HSV vers RGB
    # La saturation et valeur réglable via le Slider (utilisation d'un flag=>cf NoteBBook module)
    self.flag_color_change=0
    self.N = 512
    HSV_tuples = [(x*1.0/self.N, 0.75, 0.75) for x in range(self.N)]
    self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    # Données des couleurs ou data de chaque cell (quads) - Gestion de IHM pour le choix des couleurs
    self.cell_data,self.cd_max,self.cd_min={},{},{}
    self.TableCouleur="Z-Hauteur"
    self.cache_color={}
    self.mCacheColor()
    
    #flag concernant la texture:
    #  0 pas de changement
    # -1 texture devient inactif
    #  1 texture devient actif
    #  2 changement de texture
    #  3 changement de taille
    #cf Notebook
    self.flag_texture_change=0
       
  def OnSize(self, event):
    size = self.size = self.GetClientSize()
    if self.GetContext() and self.GetParent().IsShown() and not size[0]==0 and not size[1]==0: #vérifie que l'on est bien dans l'onglet visualisation 3D sinon warning wx canvas
        self.SetCurrent()
        gl.glViewport(0, 0, size.width, size.height)
    event.Skip()
    
  def mInitOpenGL(self,ClearColor=[0.0,0.0,0.0,1.0]):
    #Active la gestion de la profondeur
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glShadeModel (gl.GL_SMOOTH) #default gl.GL_SMOOTH (gl.GL_FLAT)
    # Fixe la perspective
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity()
    glu.gluPerspective(65.0, 4./3., 1.0, 1000.0)
    gl.glEnable(gl.GL_NORMALIZE)
    
    # Travail sur les lumières
    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR, (0.2,0.2,0.2, 1))
    gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_DIFFUSE, (1,1,1, 1))
    #gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 100.0)
    gl.glLight(gl.GL_LIGHT0,gl.GL_DIFFUSE,(1,1,1,1))
    gl.glLight(gl.GL_LIGHT0,gl.GL_SPECULAR,(1,1,1,1))   
    gl.glLight(gl.GL_LIGHT0, gl.GL_POSITION, (0,0,1000,1))
    gl.glLight(gl.GL_LIGHT1,gl.GL_DIFFUSE,(1,1,1,1))
    gl.glLight(gl.GL_LIGHT1,gl.GL_SPECULAR,(1,1,1,1))    
    gl.glLight(gl.GL_LIGHT1, gl.GL_POSITION, (0,0,-1000,1))
    gl.glEnable(gl.GL_LIGHTING)
    gl.glEnable(gl.GL_LIGHT0)
    gl.glEnable(gl.GL_LIGHT1)
    
    #Initialiser la Texture sans l'activer...
    TextureBitmap(image=r"./images/"+self._frame.m_choice_texture.LabelText,size=(10.0/float(self._frame.m_slider_texture.GetValue())))

    
    # fixe le fond d'écran à noir
    gl.glClearColor(*ClearColor)
    # prépare à travailler sur le modèle
    # (données de l'application)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    #On crée la display list
    self.mCreerDisplayList()

    
  def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.
   
  def mCacheColor(self):
    #Gestion de la couleur à l'avance,  appelé entre autre par NoteBook.OnChoice_vtk_color
    j=0
    self.cache_color[self.TableCouleur]=[]
    for i in self.points:
      if  not self.TableCouleur=="Z-Hauteur":
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((self.cell_data[self.TableCouleur][j]-self.cd_min[self.TableCouleur])/(self.cd_max[self.TableCouleur]-self.cd_min[self.TableCouleur]+1e-99)))-1])
      else:
        self.cache_color[self.TableCouleur].append(self.RGB_tuples[int(self.N*abs((i[0][2]-self.min[2])/(self.max[2]-self.min[2]+1e-99)))-1])  
      j+=1 
   
  
  def mDrawAxes(self):
    _anti_zoom=self.oCamera.r*0.1
    _flag_texture=gl.glIsEnabled(gl.GL_TEXTURE_2D)
    gl.glDisable(gl.GL_TEXTURE_2D)  
    gl.glDisable(gl.GL_DEPTH_TEST)
    gl.glDisable(gl.GL_COLOR_MATERIAL)
    gl.glDisable(gl.GL_LIGHTING)
    
    gl.glPushMatrix ()    
    gl.glTranslate(0,0,0)
    gl.glScalef(_anti_zoom,_anti_zoom,_anti_zoom)

    gl.glLineWidth (2.0)

    gl.glBegin (gl.GL_LINES)
    gl.glColor3d(1,0,0) # X axis is red.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(1,0,0 )
    gl.glEnd()
    gl.glRasterPos3f(1.2, 0.0, 0.0)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('x'))
    gl.glBegin (gl.GL_LINES)
    gl.glColor3d(0,1,0) # Y axis is green.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(0,1,0)
    gl.glEnd()    
    gl.glRasterPos3f(0.0, 1.2, 0.0)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('y'))
    gl.glBegin (gl.GL_LINES)    
    gl.glColor3d(0,0,1); # z axis is blue.
    gl.glVertex3d(0,0,0)
    gl.glVertex3d(0,0,1)
    gl.glEnd()    
    gl.glRasterPos3f(0.0, 0.0, 1.2)
    glut.glutBitmapCharacter(glut.GLUT_BITMAP_9_BY_15, ord('z'))
    gl.glPopMatrix()   
    
    if _flag_texture==True: gl.glEnable(gl.GL_TEXTURE_2D)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_COLOR_MATERIAL)
    gl.glEnable(gl.GL_LIGHTING)

  
  def mCreerDisplayList(self):
    """
    Utilisation des DisplayList d'OpenGL pour mettre en cache une scéne statique ou un objet
    Cette Fonction est appelé à l'init OpenGL puis à chaque fois que les vertex (points) ou la couleur change
    cf http://www.siteduzero.com/tutoriel-3-3841-afficher-une-display-list.html
    """
    self.dl=gl.glGenLists(1)
    gl.glNewList(self.dl,gl.GL_COMPILE)
    ################################ Création de l'objet
    j=0
    #_c1,_c2,_c3,_c4=Common.FindCorners(self.points)
    #flag1,flag2,flag3,flag4=0,0,0,0
    for i in self.points:
      gl.glColor3d(*self.cache_color[self.TableCouleur][j])
      # Boucle sur les différents sommet de l'élément (QUAD ou TRI à afficher)
      for k in i:
        #=======================================================================
        # if (k[0],k[1])==_c1 and flag1==0:
        #  gl.glTexCoord2f(1.0, 0.0)
        #  flag1=1
        # if (k[0],k[1])==_c2 and flag2==0:
        #  gl.glTexCoord2f(0.0, 0.0)
        #  flag2=1
        # if (k[0],k[1])==_c3 and  flag3==0:
        #  gl.glTexCoord2f(1.0, 1.0)
        #  flag3=1
        # if (k[0],k[1])==_c4 and flag4==0:
        #  gl.glTexCoord2f(0.0, 1.0)
        #  flag4=1                            
        #=======================================================================
        gl.glVertex3d(k[0],k[1],k[2])
      j+=1
    ################################ Création de l'objet (fin)
    gl.glEndList()
  
  def mDessine(self,event):
    """
    Fonction Principale pour dessiner la scéne "OpenGL"
    Cette fonction est la fonction callback de l'événement PAINT [self.Bind(wx.EVT_PAINT, self.mDessine)]
    Fortement utiliser dans toutes l'Application elle est appelé indirectement via la fonction Refresh(True) de l'objet oVisuOpenGL
    ATTENTION!! Chaque Ajout dans cette fonction peut ralentir l'animation OpenGL!!!
    """
    #Vérifie qu'il n'y a rien dans la queue
    if not self.q.empty()==True:
      [self.points,self.cell_data],_flag_cache,_filein=self.q.get() #on récupère les points, on récupère le flag pour savoir si les points viennent du cache ou pas
      if _flag_cache==0:# si les données ne viennent pas du cache il faut les mettre
        self._frame.cache_liste_points[_filein]=[self.points,self.cell_data]
      self.flag_new_set_of_points-=1
      self._frame.m_textCtrl_console.AppendText(".")
      self.mean,self.max,self.min=Common.MeanMaxMin(self.points) 
      #Récupération des Map de couleur dans les cell_data, mis à jour de la liste de choix couleur
      self._frame.m_choice_vtk_color.Clear()
      self._frame.m_choice_vtk_color.Append("Z-Hauteur")
      for _i in self.cell_data:
        self.cd_max[_i],self.cd_min[_i]=min(self.cell_data[_i]),max(self.cell_data[_i])
        self._frame.m_choice_vtk_color.Append(_i)
      self._frame.m_choice_vtk_color.SetSelection(0)
      self.mCacheColor()
      self.mCreerDisplayList()
    #Création de tuple de couleur HSV
    if not self.flag_color_change==0:
      #cas de changement de saturation/couleur (cf NoteBook.OnScroll_slider_vtk) ou
      HSV_tuples = [(x*1.0/self.N, float(self._frame.m_slider_vtk.GetValue())/100.0, float(self._frame.m_slider_vtk.GetValue())/100.0) for x in range(self.N)]
      HSV_tuples = Common.RotateList(HSV_tuples, self._frame.m_slider_vtk_color.GetValue())
      self.RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
      self.mCacheColor()
      self.flag_color_change=0
      self.mCreerDisplayList()
    if not self.flag_texture_change==0:
      #Cas d'un changement dans les paramêtres GUI de la texture
      #  0 pas de changement
      # -1 texture devient inactif
      #  1 texture devient actif
      #  2 changement de texture
      #  3 changement de taille
      #cf Notebook
      if self.flag_texture_change==1:
        gl.glEnable(gl.GL_TEXTURE_2D)
      if self.flag_texture_change==-1:
        gl.glDisable(gl.GL_TEXTURE_2D)   
      if self.flag_texture_change==2:    
        TextureBitmap(image=r"./images/"+self._frame.m_choice_texture.LabelText,size=(10.0/float(self._frame.m_slider_texture.GetValue())))
      if self.flag_texture_change==3:
        gl.glTexGendv(gl.GL_S,gl.GL_OBJECT_PLANE,(10.0/float(self._frame.m_slider_texture.GetValue()),0,0,0))
        gl.glTexGendv(gl.GL_T,gl.GL_OBJECT_PLANE,(0,10.0/float(self._frame.m_slider_texture.GetValue()),0,0))
      self.flag_texture_change=0
      
    #Indique que les instructions OpenGL s'adressent au contexte OpenGL courant
    self.SetCurrent()
    if not self.init:
      self.mInitOpenGL()
      self.init = True

    #initialise les données liées à la gestion de la profondeur
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # initialise GL_MODELVIEW
    # place le repère en (0,0,0)
    gl.glLoadIdentity()

    #On positionne la caméra
    if self.flag_reset_view==1:
      #cas ou l'on remet la caméra en position "moyenne" lorsque l'on clique sur le bouton Reset View (cf NoteBook)
      self.oCamera=cCamera(xy=[0.0,0.0])
      self.flag_reset_view=0
    self.oCamera.mSetVue()
    gl.glTranslate(-self.mean[0],-self.mean[1],-self.mean[2])
    
    gl.glEnable(gl.GL_LINE_SMOOTH)    
    
    
    gl.glBegin(gl.GL_QUADS)    
    gl.glCallList(self.dl)
    gl.glEnd()
    self.mDrawAxes()
    #Finalement, envoi du dessin à l écran
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
      
    if event.LeftDown():
      self.lbd=1
      self.t0=self.oCamera.theta
      self.p0=self.oCamera.phi
      
    if event.RightDown():
      self.rbd=1
      self.xx0=self.oCamera.xy[0]
      self.yy0=self.oCamera.xy[1]
      
    if self.lbd>=1:
      (self.x0,self.y0)=event.GetPosition()
      self.oCamera.theta=(self.t0+(self.y0-self.y)/100.0)
      self.oCamera.phi=(self.p0+(self.x0-self.x)/100.0)   
      self.Refresh(True)          
         
    elif self.rbd>=1:
      (self.x0,self.y0)=event.GetPosition()
      self.oCamera.xy[1]=self.yy0+(self.y0-self.y)*self.oCamera.r/200.0
      self.oCamera.xy[0]=self.xx0-(self.x0-self.x)*self.oCamera.r/200.0
      self.Refresh(True)         
    else:
      (self.x,self.y)=event.GetPosition() 
      
    if event.ButtonUp():
      self.lbd=0 
      self.rbd=0
    event.Skip()   

def TextureBitmap(image=r".\images\Mire_R.bmp",size=0.1):
  #On charge l'image texture à plaqué
  #@note: http://www.fil.univ-lille1.fr/~aubert/p3d/Cours04.pdf

  image_bmp=wx.Bitmap(image)
  ix=image_bmp.Width
  iy=image_bmp.Height
  import numpy
  image_buffer = numpy.ones((ix,iy,3), numpy.uint8)
  image_bmp.CopyToBuffer(image_buffer)
  image=image_buffer.data
  ID=gl.glGenTextures(1)
  gl.glBindTexture(gl.GL_TEXTURE_2D, ID)
  gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT,1)
  gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, ix, iy, 0,gl.GL_RGB, gl.GL_UNSIGNED_BYTE, image_buffer)
  gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
  gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
  gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_DECAL)
  gl.glTexGeni(gl.GL_S,gl.GL_TEXTURE_GEN_MODE,gl.GL_OBJECT_LINEAR)
  gl.glEnable(gl.GL_TEXTURE_GEN_S)
  gl.glTexGeni(gl.GL_T,gl.GL_TEXTURE_GEN_MODE,gl.GL_OBJECT_LINEAR)  
  gl.glEnable(gl.GL_TEXTURE_GEN_T)
  gl.glTexGendv(gl.GL_S,gl.GL_OBJECT_PLANE,(size,0,0,0))
  gl.glTexGendv(gl.GL_T,gl.GL_OBJECT_PLANE,(0,size,0,0))
  
  #gl.glEnable(gl.GL_TEXTURE_2D)
    

class cSimpleVueOpenGL(cMainVueOpenGL):
  def __init__(self, *args, **kwargs):
    cMainVueOpenGL.__init__(self, *args, **kwargs)

    #On redéfinie l'objet caméra pour un autre point de vue
    self.oCamera=cCamera(r=10,theta=math.pi/2,phi=math.pi/2,eye_view=self.mean)
    TextureBitmap()

  def mDessine(self,event):
    """
    Fonction Principale pour dessiner la scéne simple "OpenGL" (redéfinition de la fonction mDessine de la class parente)
    Cette fonction est la fonction callback de l'événement PAINT [self.Bind(wx.EVT_PAINT, self.mDessine)]
    Fortement utiliser dans toutes l'Application elle est appelé indirectement via la fonction Refresh(True) de l'objet oVisuOpenGL
    ATTENTION!! Chaque Ajout dans cette fonction peut ralentir l'animation OpenGL!!!
    """    


    #Indique que les instructions OpenGL s'adressent au contexte OpenGL courant
    self.SetCurrent()
    if not self.init:
      self._mInitOpenGL()
      self.init = True
    
    
    self.mCacheColor()
    self.mCreerDisplayList()
    
    #initialise les données liées à la gestion de la profondeur
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    # initialise GL_MODELVIEW
    # place le repère en (0,0,0)
    gl.glLoadIdentity()

    #On positionne la caméra
    if self.flag_reset_view==1:
      #cas ou l'on remet la caméra en position "moyenne" lorsque l'on clique sur le bouton Reset View (cf NoteBook)
      self.oCamera=cCamera()
      self.flag_reset_view=0
    self.oCamera.mSetVue()
    gl.glTranslate(-self.mean[0],-self.mean[1],-self.mean[2])
    
    gl.glEnable(gl.GL_LINE_SMOOTH)    
    
    
    gl.glBegin(gl.GL_QUADS)    
    gl.glCallList(self.dl)
    gl.glEnd()
    
    #Finalement, envoi du dessin à l écran
    gl.glFlush()
    self.SwapBuffers()
    pixels = gl.glReadPixels( 0,0, self.size[0],self.size[1], gl.GL_RGB, gl.GL_UNSIGNED_BYTE )
    image_bmp = Common.scale_bitmap(wx.BitmapFromBuffer(self.size[0],self.size[1],pixels),50,50)
    self.TopLevelParent.m_bitmap_test.SetBitmap(image_bmp)
    event.Skip()
    
  def _mInitOpenGL(self):
    self.mInitOpenGL([215.0/255.0,1.0,215.0/255.0,1.0])
          